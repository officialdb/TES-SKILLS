"""Unit tests for website copy and visual presentation standards in ui-ux-standards and frontend-quality."""

from pathlib import Path
import pytest

from tes.adapters import get_adapter
from tes.analyzer import SkillAnalyzer
from tes.config import get_skills_source_dir
from tes.models import InstalledSkillManifest, Scope, TargetManifest
from tes.registry import Registry
from tes.updater import Updater
from tes.validator import parse_frontmatter


@pytest.fixture
def skills_dir() -> Path:
    return get_skills_source_dir()


def test_ui_ux_standards_prohibits_decorative_blinking_dots(skills_dir: Path):
    skill_file = skills_dir / "ui-ux-standards" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Prohibits decorative animated / blinking / pulsing dots
    assert "No Decorative Animated Dots" in content
    assert "blinking" in content.lower()
    assert "pulsing" in content.lower()
    assert "cognitive distraction" in content.lower()

    # Checklist verification
    checklist_file = skills_dir / "ui-ux-standards" / "checklists" / "ui-ux-review-checklist.md"
    cl_content = checklist_file.read_text(encoding="utf-8")
    assert "blinking" in cl_content.lower() or "pulsing" in cl_content.lower()

    # Reference documentation verification
    ref_file = skills_dir / "ui-ux-standards" / "references" / "visual-design-principles.md"
    ref_content = ref_file.read_text(encoding="utf-8")
    assert "The Ban on Decorative Animated Dots" in ref_content
    assert "Cognitive Distraction" in ref_content
    assert "Alarm Mimicry" in ref_content


def test_ui_ux_standards_website_copy_avoids_em_dashes(skills_dir: Path):
    skill_file = skills_dir / "ui-ux-standards" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Preference against em dashes in website copy
    assert "Avoid Em Dashes in Website Copy" in content
    assert "—" in content
    assert "Rewrite sentences naturally" in content or "naturally" in content

    # Contains concrete rewrite examples
    assert "Avoid:" in content
    assert "Prefer:" in content

    # Context boundary preserved: technical docs, code syntax, CLI flags exempt
    assert "Technical documentation" in content
    assert "exempt" in content

    # Tone standards
    assert "Authentic, Professional Tone" in content
    assert "jargon" in content.lower()

    # Checklist verification
    checklist_file = skills_dir / "ui-ux-standards" / "checklists" / "ui-ux-review-checklist.md"
    cl_content = checklist_file.read_text(encoding="utf-8")
    assert "em dashes" in cl_content.lower()


def test_frontend_quality_css_motion_and_copy_auditing(skills_dir: Path):
    skill_file = skills_dir / "frontend-quality" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # CSS motion hygiene prohibiting decorative keyframe animations
    assert "CSS Motion Hygiene" in content
    assert "keyframes" in content.lower()
    assert "pulse" in content.lower() or "blink" in content.lower()
    assert "prefers-reduced-motion" in content

    # Status indicators must bind to reactive state
    assert "reactive state" in content.lower()

    # Template string and copy auditing
    assert "Template String & Copy Auditing" in content
    assert "em dashes" in content.lower() or "—" in content

    # Checklist verification
    checklist_file = skills_dir / "frontend-quality" / "checklists" / "frontend-performance-checklist.md"
    cl_content = checklist_file.read_text(encoding="utf-8")
    assert "pulse" in cl_content.lower() or "blink" in cl_content.lower()
    assert "em dashes" in cl_content.lower() or "—" in cl_content


def test_functional_status_indicators_remain_permitted(skills_dir: Path):
    ui_content = (skills_dir / "ui-ux-standards" / "SKILL.md").read_text(encoding="utf-8")
    fq_content = (skills_dir / "frontend-quality" / "SKILL.md").read_text(encoding="utf-8")

    # Both skills explicitly permit functional indicators communicating genuine live system state
    assert "Functional Indicators Permitted" in ui_content
    assert "Functional loading, connection, and status indicators remain permitted" in ui_content
    assert "reactive state" in fq_content.lower()


def test_no_duplicate_instruction_blocks_between_ui_skills():
    analyzer = SkillAnalyzer()
    cat_report = analyzer.analyze_catalogue()
    # Ensure no 15+ normalized word duplicate blocks were introduced
    assert len(cat_report.potential_duplicates) == 0, f"Duplicate blocks found: {cat_report.potential_duplicates}"


def test_skills_versioned_at_1_3_0(loaded_registry: Registry, skills_dir: Path):
    """Verify ui-ux-standards and frontend-quality are versioned at 1.3.0 in registry and frontmatter."""
    ui_meta = loaded_registry.get_skill("ui-ux-standards")
    fq_meta = loaded_registry.get_skill("frontend-quality")

    assert ui_meta is not None
    assert ui_meta.version == "1.3.0"

    assert fq_meta is not None
    assert fq_meta.version == "1.3.0"

    # Verify unrelated skills remain at 1.0.0
    for sid in ["engineering-core", "software-engineering", "security-audit", "devops-engineering"]:
        assert loaded_registry.get_skill(sid).version == "1.0.0"

    # Verify frontmatter version fields
    ui_fm, _, _ = parse_frontmatter((skills_dir / "ui-ux-standards" / "SKILL.md").read_text(encoding="utf-8"))
    fq_fm, _, _ = parse_frontmatter((skills_dir / "frontend-quality" / "SKILL.md").read_text(encoding="utf-8"))

    assert str(ui_fm.get("version")) == "1.3.0"
    assert str(fq_fm.get("version")) == "1.3.0"


def test_update_mechanism_identifies_1_3_0_as_newer(temp_project: Path, loaded_registry: Registry):
    """Verify TES update mechanism identifies 1.3.0 as an available update over installed 1.1.0 and 1.2.0."""
    adapter = get_adapter("opencode")
    manifest = TargetManifest(
        skills={
            "ui-ux-standards": InstalledSkillManifest(
                skill_id="ui-ux-standards",
                version="1.2.0",
                installed_at="2026-10-31T10:51:00Z",
                scope=Scope.PROJECT,
                target="opencode",
                managed_files=["SKILL.md"],
                hashes={"SKILL.md": "fakehash1"},
            ),
            "frontend-quality": InstalledSkillManifest(
                skill_id="frontend-quality",
                version="1.1.0",
                installed_at="2026-10-31T10:51:00Z",
                scope=Scope.PROJECT,
                target="opencode",
                managed_files=["SKILL.md"],
                hashes={"SKILL.md": "fakehash2"},
            ),
            "engineering-core": InstalledSkillManifest(
                skill_id="engineering-core",
                version="1.0.0",
                installed_at="2026-10-31T10:51:00Z",
                scope=Scope.PROJECT,
                target="opencode",
                managed_files=["SKILL.md"],
                hashes={"SKILL.md": "fakehash3"},
            ),
        }
    )
    adapter.write_manifest(manifest, Scope.PROJECT, temp_project)

    updater = Updater(adapter, loaded_registry, scope=Scope.PROJECT, project_root=temp_project)
    statuses = updater.check_updates()

    status_map = {s.skill_id: s for s in statuses}

    # ui-ux-standards update available (1.2.0 -> 1.3.0)
    assert status_map["ui-ux-standards"].update_available is True
    assert status_map["ui-ux-standards"].installed_version == "1.2.0"
    assert status_map["ui-ux-standards"].latest_version == "1.3.0"

    # frontend-quality update available (1.1.0 -> 1.3.0)
    assert status_map["frontend-quality"].update_available is True
    assert status_map["frontend-quality"].installed_version == "1.1.0"
    assert status_map["frontend-quality"].latest_version == "1.3.0"

    # engineering-core is up to date (1.0.0 == 1.0.0)
    assert status_map["engineering-core"].update_available is False
    assert status_map["engineering-core"].installed_version == "1.0.0"
    assert status_map["engineering-core"].latest_version == "1.0.0"


def test_ui_ux_standards_responsive_navigation_standards(skills_dir: Path):
    """Verify ui-ux-standards contains comprehensive responsive navigation standards."""
    skill_file = skills_dir / "ui-ux-standards" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Core skill coverage
    assert "Responsive Navigation Design" in content
    assert "Desktop Navigation Architecture" in content
    assert "Mobile Hamburger Menu" in content
    assert "Responsive Breakpoint Behavior" in content
    assert "Pattern Selection" in content
    assert "44x44px" in content

    # Reference documentation exists and is linked
    ref_file = skills_dir / "ui-ux-standards" / "references" / "responsive-navigation-design.md"
    assert ref_file.exists()
    assert "responsive-navigation-design.md" in content
    ref_content = ref_file.read_text(encoding="utf-8")
    assert "Foundations of Responsive Navigation" in ref_content
    assert "Navigation Archetypes" in ref_content
    assert "Dropdown Navigation" in ref_content
    assert "Slide-In Drawer" in ref_content
    assert "Full-Screen Overlay" in ref_content
    assert "Expandable Accordion" in ref_content

    # Reusable checklist exists and is linked
    cl_file = skills_dir / "ui-ux-standards" / "checklists" / "responsive-navigation-checklist.md"
    assert cl_file.exists()
    assert "responsive-navigation-checklist.md" in content
    cl_content = cl_file.read_text(encoding="utf-8")
    assert "Desktop Display" in cl_content
    assert "Mobile Hamburger" in cl_content
    assert "Escape Key Support" in cl_content
    assert "Touch Target Sizing" in cl_content


def test_frontend_quality_responsive_navigation_implementation(skills_dir: Path):
    """Verify frontend-quality contains detailed implementation standards for responsive navigation."""
    skill_file = skills_dir / "frontend-quality" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Core skill coverage
    assert "Responsive Navigation & Mobile Menu Implementation" in content
    assert "aria-label" in content
    assert "aria-expanded" in content
    assert "aria-controls" in content
    assert "Escape" in content
    assert "overflow: hidden" in content

    # Reference documentation exists and is linked
    ref_file = skills_dir / "frontend-quality" / "references" / "responsive-navigation-implementation.md"
    assert ref_file.exists()
    assert "responsive-navigation-implementation.md" in content
    ref_content = ref_file.read_text(encoding="utf-8")
    assert "Single Source of Truth" in ref_content
    assert "Body Scroll Locking" in ref_content
    assert "Escape Key Dismissal" in ref_content
    assert "Single Source of Navigation Items" in ref_content
    assert "Zero Layout Shifts (CLS < 0.1)" in ref_content


def test_ui_ux_standards_dashboard_and_landing_page_references(skills_dir: Path):
    """Verify ui-ux-standards contains comprehensive references for dashboard and landing page design."""
    skill_file = skills_dir / "ui-ux-standards" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Main SKILL.md integration
    assert "dashboard-design-principles.md" in content
    assert "landing-page-design-principles.md" in content
    assert "component-library-design-guidelines.md" in content

    # Dashboard reference verification (Reference A)
    dash_file = skills_dir / "ui-ux-standards" / "references" / "dashboard-design-principles.md"
    assert dash_file.exists()
    dash_text = dash_file.read_text(encoding="utf-8")
    assert "Grounded Observations" in dash_text
    assert "Persistent Vertical Left Sidebar" in dash_text
    assert "Three-Column Desktop Workspace" in dash_text
    assert "Analytics & Progress" in dash_text
    assert "Time Tracker" in dash_text
    assert "Domain & Product Adaptability" in dash_text

    # Landing page reference verification (Reference B)
    lp_file = skills_dir / "ui-ux-standards" / "references" / "landing-page-design-principles.md"
    assert lp_file.exists()
    lp_text = lp_file.read_text(encoding="utf-8")
    assert "Centered Editorial Hero Composition" in lp_text
    assert "Conversion Action Hierarchy" in lp_text
    assert "Product-Led Visual Showcase" in lp_text
    assert "Floating Metric Badge" in lp_text
    assert "Editorial Typography Contrast" in lp_text

    # Component library design guidelines
    lib_file = skills_dir / "ui-ux-standards" / "references" / "component-library-design-guidelines.md"
    assert lib_file.exists()
    lib_text = lib_file.read_text(encoding="utf-8")
    assert "Libraries as Implementation Resources, Not Design Strategies" in lib_text
    assert "Never Accept Default Library Themes Unconditionally" in lib_text
    assert "No Decorative Animated Dots" in lib_text


def test_frontend_quality_component_library_and_layout_references(skills_dir: Path):
    """Verify frontend-quality contains detailed implementation guides for libraries, dashboards, and landing pages."""
    skill_file = skills_dir / "frontend-quality" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Main SKILL.md integration
    assert "frontend-component-library-selection.md" in content
    assert "dashboard-layout-implementation.md" in content
    assert "landing-page-implementation.md" in content

    # Library selection guide verification
    lib_sel = skills_dir / "frontend-quality" / "references" / "frontend-component-library-selection.md"
    assert lib_sel.exists()
    lib_sel_text = lib_sel.read_text(encoding="utf-8")
    assert "The 10-Point Library Selection Checklist" in lib_sel_text
    assert "shadcn/ui" in lib_sel_text
    assert "Flowbite" in lib_sel_text
    assert "Radix UI" in lib_sel_text
    assert "Existing vs. Custom Components" in lib_sel_text

    # Dashboard layout implementation verification
    dash_impl = skills_dir / "frontend-quality" / "references" / "dashboard-layout-implementation.md"
    assert dash_impl.exists()
    dash_impl_text = dash_impl.read_text(encoding="utf-8")
    assert "Multi-Column Dashboard Layout Architecture" in dash_impl_text
    assert "ProgressRing" in dash_impl_text
    assert "Accessible Bar Charts" in dash_impl_text
    assert "Digital Timer Widget & Interval Hygiene" in dash_impl_text

    # Landing page implementation verification
    lp_impl = skills_dir / "frontend-quality" / "references" / "landing-page-implementation.md"
    assert lp_impl.exists()
    lp_impl_text = lp_impl.read_text(encoding="utf-8")
    assert "Centered Hero Section Architecture" in lp_impl_text
    assert "overflow-x: clip" in lp_impl_text
    assert "Responsive Product Mockup Container" in lp_impl_text
    assert "Optimizing Core Web Vitals on Landing Pages" in lp_impl_text


def test_ui_ux_standards_ecommerce_references(skills_dir: Path):
    """Verify ui-ux-standards contains comprehensive references for e-commerce storefronts and product detail pages."""
    skill_file = skills_dir / "ui-ux-standards" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Main SKILL.md integration
    assert "ecommerce-design-principles.md" in content
    assert "E-Commerce Storefront Composition" in content
    assert "Product Detail Page Architecture" in content
    assert "Context-Sensitive Domain Design" in content

    # E-commerce reference verification
    ecom_file = skills_dir / "ui-ux-standards" / "references" / "ecommerce-design-principles.md"
    assert ecom_file.exists()
    ecom_text = ecom_file.read_text(encoding="utf-8")
    assert "ZenVora E-commerce Storefront" in ecom_text
    assert "SoundWave Product Detail Page" in ecom_text
    assert "Direct Observations (Confirmed from Source)" in ecom_text
    assert "Inferred Recommendations" in ecom_text
    assert "Limitations of Reference A" in ecom_text
    assert "Limitations of Reference B" in ecom_text
    assert "Product Discovery & Product Card Design" in ecom_text
    assert "Buying Decision Hierarchy" in ecom_text
    assert "Context-Sensitive Design: Domain Adaptability" in ecom_text

    # Checklist verification
    cl_file = skills_dir / "ui-ux-standards" / "checklists" / "ui-ux-review-checklist.md"
    cl_text = cl_file.read_text(encoding="utf-8")
    assert "storefront product cards" in cl_text.lower()
    assert "product detail page (pdp)" in cl_text.lower()


def test_frontend_quality_ecommerce_references(skills_dir: Path):
    """Verify frontend-quality contains detailed implementation standards for e-commerce grids, galleries, and vitals."""
    skill_file = skills_dir / "frontend-quality" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Main SKILL.md integration
    assert "ecommerce-implementation.md" in content
    assert "E-Commerce Architecture & Performance" in content

    # E-commerce implementation guide verification
    impl_file = skills_dir / "frontend-quality" / "references" / "ecommerce-implementation.md"
    assert impl_file.exists()
    impl_text = impl_file.read_text(encoding="utf-8")
    assert "Responsive Grid Reflow Mechanics" in impl_text
    assert "Product Image Gallery Synchronization" in impl_text
    assert "Variant Selection (Color & Size)" in impl_text
    assert "Bounded Quantity Controls" in impl_text
    assert "Conversion Actions & Mutation Lifecycle" in impl_text
    assert "Optimistic Updates & Rollback" in impl_text
    assert "Accessible Tabbed Content" in impl_text
    assert "Preventing Cumulative Layout Shift (CLS < 0.1)" in impl_text
    assert "Viewport-Driven Image Priority" in impl_text
    assert "AbortController" in impl_text

    # Checklist verification
    cl_file = skills_dir / "frontend-quality" / "checklists" / "frontend-performance-checklist.md"
    cl_text = cl_file.read_text(encoding="utf-8")
    assert "aspect ratio containers" in cl_text.lower()
    assert "viewport visibility" in cl_text.lower()
    assert "optimistic rollback" in cl_text.lower()


