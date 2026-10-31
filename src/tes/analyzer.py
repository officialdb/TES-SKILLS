"""Token efficiency diagnostics and skill catalogue analysis engine for TES."""

from dataclasses import dataclass, field
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple
import yaml

from tes.config import get_registry_dir, get_skills_source_dir
from tes.registry import Registry
from tes.validator import parse_frontmatter, MARKDOWN_LINK_PATTERN

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")

    def estimate_tokens(text: str) -> int:
        return len(_ENC.encode(text))

    TOKENIZER_METHOD = "tiktoken (cl100k_base)"
except Exception:
    def estimate_tokens(text: str) -> int:
        # Standard fallback heuristic (~4 chars/token)
        return max(1, len(text) // 4)

    TOKENIZER_METHOD = "heuristic (~4 characters per token)"


@dataclass
class SkillAnalysis:
    skill_id: str
    name: str
    category: str
    description: str
    desc_words: int
    desc_chars: int
    long_description: bool
    skill_md_size_bytes: int
    skill_md_lines: int
    skill_md_words: int
    skill_md_approx_tokens: int
    references_count: int
    checklists_count: int
    templates_count: int
    scripts_count: int
    total_reference_files: int
    total_reference_bytes: int
    total_reference_approx_tokens: int
    broken_references: List[str] = field(default_factory=list)
    cross_references: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class CatalogueReport:
    tokenizer_method: str
    skills_count: int
    total_skill_md_bytes: int
    total_skill_md_words: int
    total_skill_md_tokens: int
    total_reference_files: int
    total_reference_bytes: int
    total_reference_tokens: int
    total_catalogue_tokens: int
    skills: List[SkillAnalysis] = field(default_factory=list)
    largest_skills: List[SkillAnalysis] = field(default_factory=list)
    potential_duplicates: List[Dict[str, Any]] = field(default_factory=list)
    broken_references: List[Tuple[str, str]] = field(default_factory=list)
    long_descriptions: List[str] = field(default_factory=list)


class SkillAnalyzer:
    """Analyzes TES skills for token efficiency, size, and progressive disclosure."""

    def __init__(self, skills_dir: Optional[Path] = None, registry: Optional[Registry] = None):
        self.skills_dir = skills_dir or get_skills_source_dir()
        self.registry = registry or Registry(get_registry_dir(), self.skills_dir)
        try:
            self.registry.load()
        except Exception:
            pass

    def analyze_single_skill(self, skill_dir: Path) -> SkillAnalysis:
        skill_id = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        category = "engineering"
        reg_skill = self.registry.get_skill(skill_id)
        if reg_skill:
            category = reg_skill.category

        if not skill_md.exists():
            return SkillAnalysis(
                skill_id=skill_id,
                name=skill_id,
                category=category,
                description="",
                desc_words=0,
                desc_chars=0,
                long_description=False,
                skill_md_size_bytes=0,
                skill_md_lines=0,
                skill_md_words=0,
                skill_md_approx_tokens=0,
                references_count=0,
                checklists_count=0,
                templates_count=0,
                scripts_count=0,
                total_reference_files=0,
                total_reference_bytes=0,
                total_reference_approx_tokens=0,
                warnings=["Missing SKILL.md"],
            )

        content = skill_md.read_text(encoding="utf-8")
        size_bytes = len(content.encode("utf-8"))
        lines_count = len(content.splitlines())
        words_count = len(content.split())
        approx_tokens = estimate_tokens(content)

        frontmatter, body, err = parse_frontmatter(content)
        name = frontmatter.get("name", skill_id) if frontmatter else skill_id
        description = frontmatter.get("description", "") if frontmatter else ""
        desc_words = len(description.split())
        desc_chars = len(description)

        # Flag unusually long metadata descriptions (>200 chars or >40 words)
        long_desc = desc_chars > 200 or desc_words > 40
        warnings = []
        if err:
            warnings.append(f"Frontmatter error: {err}")
        if long_desc:
            warnings.append(f"Lengthy frontmatter description ({desc_chars} chars, {desc_words} words)")

        # Count references, checklists, templates, scripts
        ref_files = list((skill_dir / "references").glob("*.md")) if (skill_dir / "references").exists() else []
        chk_files = list((skill_dir / "checklists").glob("*.md")) if (skill_dir / "checklists").exists() else []
        tpl_files = list((skill_dir / "templates").glob("*")) if (skill_dir / "templates").exists() else []
        scr_files = list((skill_dir / "scripts").glob("*")) if (skill_dir / "scripts").exists() else []

        all_secondary = [f for f in ref_files + chk_files + tpl_files + scr_files if f.is_file()]
        ref_bytes = sum(len(f.read_bytes()) for f in all_secondary)
        ref_tokens = sum(estimate_tokens(f.read_text(encoding="utf-8", errors="ignore")) for f in all_secondary)

        # Check local file references in body
        broken_refs = []
        for match in MARKDOWN_LINK_PATTERN.finditer(body):
            ref = match.group(1).split("#")[0].strip()
            if ref and not ref.startswith("/") and not ref.startswith("http"):
                target = skill_dir / ref
                if not target.exists():
                    broken_refs.append(ref)
                    warnings.append(f"Broken link: {ref}")

        # Check mentions of other skills (cross-dependencies)
        all_skill_ids = {s.id for s in self.registry.list_skills()} if self.registry.list_skills() else set()
        cross_refs = []
        for other_id in all_skill_ids:
            if other_id != skill_id and other_id in body:
                cross_refs.append(other_id)

        return SkillAnalysis(
            skill_id=skill_id,
            name=name,
            category=category,
            description=description,
            desc_words=desc_words,
            desc_chars=desc_chars,
            long_description=long_desc,
            skill_md_size_bytes=size_bytes,
            skill_md_lines=lines_count,
            skill_md_words=words_count,
            skill_md_approx_tokens=approx_tokens,
            references_count=len(ref_files),
            checklists_count=len(chk_files),
            templates_count=len(tpl_files),
            scripts_count=len(scr_files),
            total_reference_files=len(all_secondary),
            total_reference_bytes=ref_bytes,
            total_reference_approx_tokens=ref_tokens,
            broken_references=broken_refs,
            cross_references=cross_refs,
            warnings=warnings,
        )

    def analyze_catalogue(
        self, skill_filter: Optional[str] = None, bundle_filter: Optional[str] = None
    ) -> CatalogueReport:
        skill_dirs = [p for p in self.skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]

        # Apply filters
        if skill_filter:
            skill_dirs = [p for p in skill_dirs if p.name == skill_filter]
        elif bundle_filter:
            bundle_skills, _ = self.registry.resolve_skills_to_install(bundle_filter)
            allowed_ids = {s.id for s in bundle_skills}
            skill_dirs = [p for p in skill_dirs if p.name in allowed_ids]

        analyses: List[SkillAnalysis] = []
        broken_all: List[Tuple[str, str]] = []
        long_descs: List[str] = []

        for sdir in sorted(skill_dirs, key=lambda p: p.name):
            analysis = self.analyze_single_skill(sdir)
            analyses.append(analysis)
            for br in analysis.broken_references:
                broken_all.append((analysis.skill_id, br))
            if analysis.long_description:
                long_descs.append(analysis.skill_id)

        # Detect duplicated instructions across skills
        duplicates = self._find_duplicate_instruction_blocks(analyses)

        # Aggregations
        tot_md_bytes = sum(a.skill_md_size_bytes for a in analyses)
        tot_md_words = sum(a.skill_md_words for a in analyses)
        tot_md_tokens = sum(a.skill_md_approx_tokens for a in analyses)
        tot_ref_files = sum(a.total_reference_files for a in analyses)
        tot_ref_bytes = sum(a.total_reference_bytes for a in analyses)
        tot_ref_tokens = sum(a.total_reference_approx_tokens for a in analyses)

        largest = sorted(analyses, key=lambda a: a.skill_md_approx_tokens, reverse=True)

        return CatalogueReport(
            tokenizer_method=TOKENIZER_METHOD,
            skills_count=len(analyses),
            total_skill_md_bytes=tot_md_bytes,
            total_skill_md_words=tot_md_words,
            total_skill_md_tokens=tot_md_tokens,
            total_reference_files=tot_ref_files,
            total_reference_bytes=tot_ref_bytes,
            total_reference_tokens=tot_ref_tokens,
            total_catalogue_tokens=tot_md_tokens + tot_ref_tokens,
            skills=analyses,
            largest_skills=largest[:5],
            potential_duplicates=duplicates,
            broken_references=broken_all,
            long_descriptions=long_descs,
        )

    def _find_duplicate_instruction_blocks(self, analyses: List[SkillAnalysis]) -> List[Dict[str, Any]]:
        """Identify potential duplicated instruction paragraphs across multiple skills."""
        paragraphs_by_skill: Dict[str, Set[str]] = {}
        for a in analyses:
            skill_md = self.skills_dir / a.skill_id / "SKILL.md"
            if not skill_md.exists():
                continue
            text = skill_md.read_text(encoding="utf-8", errors="ignore")
            _, body, _ = parse_frontmatter(text)

            # Extract normalized paragraphs of 15+ words
            paras = set()
            for p in body.split("\n\n"):
                cleaned = re.sub(r"\s+", " ", p).strip()
                words = cleaned.split()
                if len(words) >= 15 and not cleaned.startswith("#"):
                    # Normalize simple punctuation
                    norm = re.sub(r"[^\w\s]", "", cleaned.lower())
                    paras.add(norm)
            paragraphs_by_skill[a.skill_id] = paras

        duplicates = []
        skill_ids = list(paragraphs_by_skill.keys())
        for i in range(len(skill_ids)):
            s1 = skill_ids[i]
            for j in range(i + 1, len(skill_ids)):
                s2 = skill_ids[j]
                shared = paragraphs_by_skill[s1].intersection(paragraphs_by_skill[s2])
                if shared:
                    duplicates.append({
                        "skill_1": s1,
                        "skill_2": s2,
                        "shared_blocks_count": len(shared),
                        "sample": list(shared)[0][:120] + "..." if shared else "",
                    })
        return duplicates

    def generate_report_markdown(self, report: CatalogueReport) -> str:
        """Generate a structured Markdown diagnostic report."""
        lines = [
            "# TES Token Efficiency & Skill Diagnostics Report",
            "",
            f"- **Tokenizer Methodology:** `{report.tokenizer_method}` (Approximate estimation)",
            f"- **Skills Analyzed:** {report.skills_count}",
            f"- **Total Core SKILL.md Tokens:** {report.total_skill_md_tokens:,} tokens ({report.total_skill_md_words:,} words)",
            f"- **Total Reference Material Tokens:** {report.total_reference_tokens:,} tokens ({report.total_reference_files} secondary files)",
            f"- **Full Catalogue Footprint:** {report.total_catalogue_tokens:,} tokens",
            "",
            "## 1. Skill Sizing & Instruction Budgets",
            "",
            "| Skill ID | Category | SKILL.md Words | Approx Tokens | References | Desc Length | Status |",
            "|---|---|---|---|---|---|---|",
        ]

        for s in report.skills:
            status = "Optimal"
            if s.warnings:
                status = f"Review ({len(s.warnings)} warning)"
            lines.append(
                f"| `{s.skill_id}` | {s.category} | {s.skill_md_words:,} | {s.skill_md_approx_tokens:,} | "
                f"{s.total_reference_files} files ({s.total_reference_approx_tokens:,} tok) | "
                f"{s.desc_words}w ({s.desc_chars}c) | {status} |"
            )

        lines.extend([
            "",
            "## 2. Largest Skill Instructions",
            "",
        ])
        for s in report.largest_skills:
            lines.append(f"- **`{s.skill_id}`**: {s.skill_md_words:,} words (~{s.skill_md_approx_tokens:,} tokens)")

        lines.extend([
            "",
            "## 3. Duplication & Overlap Diagnostics",
            "",
        ])
        if report.potential_duplicates:
            lines.append(f"Found {len(report.potential_duplicates)} pair(s) with overlapping instruction blocks:")
            for d in report.potential_duplicates:
                lines.append(f"- `{d['skill_1']}` <-> `{d['skill_2']}`: {d['shared_blocks_count']} shared paragraph(s)")
                lines.append(f"  *Sample:* {d['sample']}")
        else:
            lines.append("✓ Zero duplicated instruction blocks detected across skills.")

        lines.extend([
            "",
            "## 4. Metadata & Reference Integrity",
            "",
            f"- Broken References: {len(report.broken_references)}",
            f"- Unusually Long Descriptions (>200 chars or >40 words): {len(report.long_descriptions)}",
        ])
        if report.broken_references:
            for sid, br in report.broken_references:
                lines.append(f"  - `{sid}`: Missing target `{br}`")
        if report.long_descriptions:
            lines.append(f"  - Lengthy metadata: {', '.join(report.long_descriptions)}")

        return "\n".join(lines)

