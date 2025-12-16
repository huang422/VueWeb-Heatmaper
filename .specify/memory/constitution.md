<!--
Sync Impact Report:
- Version change: N/A (initial) → 1.0.0
- Modified principles: None (initial creation)
- Added sections:
  * Core Principles (5 principles)
  * Technology Stack Constraints
  * Quality Standards
  * Governance
- Removed sections: None
- Templates requiring updates:
  ✅ plan-template.md - reviewed, compatible
  ✅ spec-template.md - reviewed, compatible
  ✅ tasks-template.md - reviewed, compatible
- Follow-up TODOs: None
-->

# Store Heatmap Visualization Constitution

## Core Principles

### I. Frontend-Backend Separation

The application MUST maintain clear separation between Vue.js frontend and FastAPI backend:
- Frontend handles all UI/UX, user interactions, and data visualization rendering
- Backend handles all data processing, analysis, and business logic
- Communication exclusively through RESTful API with documented contracts
- No business logic in frontend; no UI rendering in backend

**Rationale**: Enables independent development, testing, and deployment of frontend and backend. Facilitates future scaling and technology migration if needed.

### II. Data-Driven Visualization

All visualizations MUST be driven by processed data from the backend:
- Raw data processing happens in FastAPI backend
- Frontend receives clean, structured JSON for rendering
- Visualization libraries (e.g., D3.js, ECharts, Chart.js) operate on backend-provided data structures
- No raw CSV/data file parsing in frontend

**Rationale**: Centralizes data transformation logic, ensures consistency, and prevents duplicate processing. Maintains performance by preprocessing data server-side.

### III. Standalone Executable Packaging

The final application MUST be packaged as a standalone Windows executable:
- Backend packaged using PyInstaller or similar tool
- Frontend bundled and served as static assets
- Single EXE that launches embedded web server and opens browser
- No external dependencies required for end users

**Rationale**: Simplifies distribution and deployment for non-technical users. Eliminates installation complexity and environment configuration issues.

### IV. Interactive User Experience

All visualizations MUST support interactive exploration:
- Heatmap supports zooming, panning, and drill-down
- User can filter data by time, location, categories
- Real-time updates when changing visualization parameters
- Responsive design for different screen sizes

**Rationale**: Enables users to discover insights through exploration. Interactive visualizations provide more value than static reports.

### V. Performance & Responsiveness

The application MUST maintain responsive performance:
- Initial load time under 3 seconds for typical datasets
- Visualization rendering under 1 second after data changes
- Backend API responses under 500ms for data queries
- Support datasets up to 100,000 data points without degradation

**Rationale**: Poor performance destroys user experience. Data analysis tools must respond quickly to maintain user flow and enable rapid exploration.

## Technology Stack Constraints

**Mandatory Technologies**:
- **Frontend**: Vue.js 3.x with Composition API
- **Backend**: FastAPI with Python 3.9+
- **Data Processing**: Pandas for data manipulation
- **Visualization**: Modern charting library (D3.js, ECharts, or Chart.js)
- **Packaging**: PyInstaller for EXE generation

**Prohibited Patterns**:
- Do NOT use server-side rendering (SSR) - frontend is SPA only
- Do NOT embed database engines - use file-based storage or in-memory processing
- Do NOT introduce heavyweight frameworks beyond specified stack
- Do NOT use deprecated Vue.js Options API

**Rationale**: Consistency in technology choices simplifies development, reduces complexity, and ensures the team can maintain expertise. Prohibitions prevent common pitfalls that conflict with standalone EXE packaging requirements.

## Quality Standards

### Code Organization

- Backend code in `backend/` directory with `src/` and `tests/` subdirectories
- Frontend code in `frontend/` directory with standard Vue project structure
- Shared data models documented in `specs/` directory
- API contracts defined in `specs/contracts/`

### Testing Requirements

- Backend API endpoints MUST have contract tests validating request/response schemas
- Data processing functions MUST have unit tests with sample datasets
- Frontend components MAY have unit tests (not mandatory for MVP)
- Integration tests verifying frontend-backend communication are RECOMMENDED

### Documentation Requirements

- API endpoints documented with OpenAPI/Swagger (FastAPI automatic)
- README MUST include build instructions for development and EXE packaging
- User guide for the packaged application in `docs/user-guide.md`
- Data format specifications in `docs/data-format.md`

## Governance

**Amendment Process**:
- Constitution changes require documentation of rationale
- Version bump follows semantic versioning
- Template updates MUST be propagated when constitution changes

**Compliance Verification**:
- All feature specifications checked against principles during `/speckit.specify`
- Implementation plans validated in `/speckit.plan` Constitution Check section
- Violations MUST be justified in Complexity Tracking table

**Simplicity Enforcement**:
- Complexity that violates principles requires explicit justification
- Default answer to "should we add X?" is NO unless clearly needed
- Prefer simple solutions over configurable/extensible solutions

**Version**: 1.0.0 | **Ratified**: 2025-12-15 | **Last Amended**: 2025-12-15
