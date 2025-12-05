# Detailed Changelog (Technical Documentation) EN

*Complete technical changelog with implementation details*

## v1.0 (2025-07) - Foundation Release
Initial Python terminal-based implementation with core pharmacokinetic engine.

**Core Features:**
- Basic Widmark formula implementation with Watson TBW calculation
- CSV database with 52 IBA cocktails (Classic, Contemporary, New Era categories)
- Single and multiple drink BAC calculations with time progression
- Stomach condition modifier (-30% absorption when full)
- Terminal-based interactive menu system (7 options)
- Personalized cocktail modification with ingredient substitution
- Legal status classification with Italian driving limits

**Technical Implementation:**
- Weighted volume formula for alcohol graduation calculation
- Raw TBW-corrected Widmark factors for improved accuracy
- Timeline simulation with linear elimination modeling
- Category-based cocktail browsing and search functionality

---

## v2.0 (2025-08) - First Web Release
Major update: Advanced pharmacokinetic algorithm with fitness parameter.

**Algorithm Improvements:**
- Implemented distributed absorption model for multiple drinks
- Added fitness level parameter (sedentary/active/athlete) with +15-25% metabolism boost
- Temporal distribution of ingestions instead of single bolus
- Superposition principle for individual drink contributions
- Improved accuracy: reduced error from 71% to 27% in real-world testing
- Enhanced timeline predictions with continuous elimination modeling

**Database Expansion:**
- Added 10 beer types (small/medium formats) with accurate ABV
- Added 6 wine categories with standard serving sizes
- Enhanced time formatting for better UX

**Validation:**
- Real-world breathalyzer comparison tests
- Error margin reduction from 71% → 27%

---

## v3.0 (2025-08) - Full Web Application Architecture
Complete architectural transformation with production-ready features.

**Architectural Changes:**
- Extended database: 150+ beverages including cocktails, aperitifs, beers, wines
- Mobile-First design: touch-optimized responsive layout with CSS Grid/Flexbox
- Three-section architecture: Search / BAC Calculator / Database
- Single-file self-contained HTML/CSS/JavaScript application
- No external dependencies or installation requirements
- Privacy-focused: all calculations performed locally
- Cross-browser compatibility (Chrome 80+, Firefox 75+, Safari 13+)

**Scientific Enhancements:**
- Advanced fitness modeling: Sedentary/Active/Athlete levels with metabolic corrections
- Acute exercise effects: same-day workout impact on elimination rates (-1%)
- Hydration parameters: 4-level system affecting BAC dilution (±2.5%)
- Enhanced TBW calculations with fitness-based corrections
- Exercise-induced metabolism modifications
- Improved error margins through multi-factor calibration

**Regional Specialties:**
- Te+ cocktail (Origin Bar Bassano) - 9.5% ABV tea-peach extract
- Leone aperitif - Traditional Veneto alternative to Americano
- Corrected Spritz variations (Classic vs Venetian preparations)

---

## v3.4 (2025-09) - UX Enhancement
**BAC Section Redesign:**
- Transformed fitness level selector from dropdown to visual card-based selection
- Improved touch feedback for mobile interactions
- Enhanced visual hierarchy for better usability
- Reduced interaction steps for faster input

**Technical Details:**
- Replaced `<select>` element with clickable card grid
- CSS transitions for smooth selection states
- Mobile-optimized touch targets (min 44px)

---

## v3.7 (2025-09) - Explore Prototype
**First Attempt at Recommendation System:**
- Renamed "Lista" (full database) section → "Esplora" (Explore)
- Added category and ABV filters
- Implemented sorting options: alphabetical, ABV ascending/descending
- Basic comparison feature: up to 3 cocktails with descriptive phrase output

**Features:**
- Dynamic filtering system
- Multi-criteria sorting
- Simple comparison logic (category-based matching)

**Limitations Identified:**
- Comparison too simplistic (text-only output)
- No intelligent matching algorithm
- Limited personalization

---

## v3.8 (2025-09) - Failed Experiment
**Attempted Features:**
- Emoji-based category grouping for visual organization
- Reorganized drink database with hierarchical structure
- Enhanced visual taxonomy

**Outcome:**
- **Abandoned** due to manifested uselessness
- UX confusion: too many visual elements competing for attention
- None of new visual elements served any purpose
- Reverted to v3.7 stable base

**Lessons Learned:**
- Prioritize clarity over visual novelty
- Test UX changes incrementally
- Maintain fallback versions

---

## v3.9 (2025-09) - Quiz Foundation
**Complete Explore Redesign:**
- Fully functional quiz system (2 questions initially)
  - Question 1: Preferred taste (sweet/bitter/sour/dry/balanced)
  - Question 2: Alcohol intensity (light/medium/strong)
- Basic scoring algorithm for result ranking
- Progressive question reveal

**BAC Section Improvements:**
- Autocomplete dropdown while typing drink name
- Real-time suggestions from database
- Improved input validation

**Results Display Redesign:**
- Enhanced BAC results card layout
- Added loading percentage indicator with visual progress bar
- Smooth animations for result appearance

**Technical Implementation:**
- JavaScript-based quiz state management
- Fuzzy search algorithm for autocomplete
- CSS animations for loading states

---

## v4.0 (2025-10) - Quiz Enhancement
**Quiz Expansion:**
- Extended to 5 questions with progressive reveal
- Improved question flow logic
- Enhanced scoring system with weighted preferences

**Results Interface:**
- Expandable result cards with detailed information
- Info button ("i") → redirects to "Cerca" section for full drink details
- Smooth expand/collapse animations

**Matching Algorithm:**
- Complete rewrite of scoring logic
- Multi-criteria matching (taste, aroma, intensity, body)
- Weighted scoring based on preference strength

**Bug Fixes:**
- Resolved BAC calculation edge cases
- Fixed quiz navigation issues
- Improved cross-browser compatibility

---

## v4.3 (2025-10) - Explore Architecture
**Welcome Page System:**
- Introduced three exploration paths:
  1. **"Cosa ti va di bere?"** (What do you feel like?) - Guided Quiz [IMPLEMENTED]
  2. **"Percorsi di Degustazione"** (Tasting Journeys) - Curated collections [PLACEHOLDER]
  3. **"Cosa posso creare?"** (What can I create?) - Ingredient-based builder [PLACEHOLDER]

**UI/UX Improvements:**
- Card-based navigation for exploration paths
- Visual icons and descriptions
- Consistent design language across paths

**Architecture:**
- Modular structure for future path implementations
- Scalable navigation system
- View management preparation

**Database Expansion:**
- Extended to 400+ drinks
- Added preliminary sensory profiles

---

## v4.4 (2025-10) - Multi-Select Revolution ⭐
**Major Feature: Priority-Based Multi-Selection**
- Multi-select with intensity levels (★, ★★, ★★★) for:
  - Cocktail aromas (fruity, citrus, floral, herbal, savory, spicy, smoky)
  - Spirit character (sweet, dry, spicy, smoky, peaty, fruity, herbal)
- Priority-based scoring system:
  - Priority 1 (★): Basic interest → +10 points
  - Priority 2 (★★): Important preference → +20 points
  - Priority 3 (★★★): Essential characteristic → +35 points

**UI Innovation:**
- "Le tue preferenze" (Your Preferences) box - real-time summary of selections
- Visual priority indicators with color coding
- Chip-based selection interface
- Smooth transitions between priority levels

**Database Evolution:**
- Expanded to 500+ beverages
- Added comprehensive sensory tags for all drinks
- Enhanced tasting notes for spirits

**Technical Challenges:**
- Complex state management for multi-level selections
- Priority cycling logic (0 → 1 → 2 → 3 → 0)
- Score calculation with weighted priorities

**Known Issues (v4.4-prove):**
- "Restart Quiz" and "Back to Menu" buttons non-functional
- Safari compatibility issues with event handling
- State persistence problems

---

## v4.4-prove, v4.4-prove-2, v4.5, v4.6 (2025-10) - Development Hell
**Failed Attempts to Fix Critical Bugs:**

**v4.4-prove:**
- Attempted fix for quiz navigation buttons
- Introduced new bugs: quiz state corruption
- Results display broken

**v4.4-prove-2:**
- Partial progress on button functionality
- BAC calculation still broken
- Quiz restart causing page reload

**v4.5, v4.6:**
- Complete regression from v4.4-prove-2
- Lost priority-selection functionality
- Navigation completely broken
- Inconsistent behavior across browsers

I abandoned iterative fixes and committed to **complete refactor** for v4.7

---

## v4.7 (2025-11) - Clean Refactor ⭐
**Complete Code Modernization:**
- Total refactoring with modern JavaScript patterns
- Event delegation throughout application
- Centralized state management
- Modular architecture (ViewManager, QuizStateManager)
- 100% visual and functional compatibility maintained

**Fixed Critical Issues:**
- ✅ "Restart Quiz" button fully functional
- ✅ "Back to Menu" button working correctly
- ✅ Quiz state persistence across navigation
- ✅ Safari compatibility issues resolved
- ✅ BAC calculation accuracy restored

**Architecture Improvements:**
- ViewManager class for centralized view control
- QuizStateManager for quiz data handling
- Event delegation pattern for all interactions
- Reduced code duplication by ~40%

**BAC Section Redesign:**
- Inline add/remove for drink quantities
- Delete button for individual drinks
- Improved summary display
- Enhanced loading animation for calculation

**Quiz Results Enhancement:**
- "Add" button: turns green when pressed, transfers drink to BAC section
- "Compare" button: saves drink for comparison (functionality in v4.9)
- Persistent selection states
- Smooth state transitions

**Code Quality:**
- Comprehensive error handling
- Console logging for debugging
- Documented function signatures
- Consistent naming conventions

---

## v4.9 (2025-11) - Comparison System ⭐
**Advanced Comparison Engine:**
- Compare up to 5 drinks simultaneously
- Persistent comparison memory across different quiz sessions
- Smart drink tracking with duplicate prevention

**Comparison Welcome Page:**
- Visual summary of selected drinks
- Individual drink removal option
- "Clear All" functionality
- Direct link to detailed comparison

**Detailed Comparison View:**
- **Desktop Mode:** Side-by-side table layout
  - All metrics visible simultaneously
  - Sortable columns
  - Print-friendly format
  
- **Mobile Mode:** Instagram Stories-style swipeable cards
  - One drink per card
  - Swipe navigation with visual indicators
  - Touch-optimized interactions

**Comparison Metrics:**
- Category (Cocktail/Spirit/Beer/Wine)
- ABV (Alcohol by Volume)
- Pure alcohol content (grams)
- Main taste profile
- Calories per serving
- Estimated cost
- Preparation complexity
- Glassware type

**Visual Enhancements:**
- MIN values highlighted in green
- MAX values highlighted in red
- Applies to: ABV, pure alcohol, calories
- Clear visual hierarchy

**Search Section Redesign:**
- Complete layout overhaul with modern card design
- Glassmorphism UI elements
- Improved spacing and typography
- Enhanced mobile responsiveness
- Better visual hierarchy

**Info Button Enhancement:**
- Opens detailed card in overlay (modal)
- No longer redirects to Search section
- Maintains user's current context
- Preserves quiz/comparison state
- Smooth modal animations

**Technical Implementation:**
- LocalStorage for comparison persistence
- Optimized card rendering for mobile swipe
- Intersection Observer for lazy loading
- CSS Grid for responsive layout

---

## v5.0 (2025-11) - Advanced Rule-Based Matching System ⭐
**Complete Matching System Rewrite:**
- Rebuilt algorithm from ground up
- 2-level tag system (primary/secondary) for spirits
- Sophisticated penalty system for mismatches
- Normalized scoring 0-100 with clear classification:
  - Perfect Match ≥ 72 points
  - Good Choice ≥ 60 points
  - Alternative ≥ 45 points
  - Not Recommended < 45 points

**Advanced Tag System:**
**For Spirits (2-tier system):**
- Primary tags: Strong keywords in tasting notes (e.g., "sweet", "peaty", "spicy")
- Secondary tags: Mentioned characteristics (e.g., "soft", "elegant", "refined")
- Different scoring weights: Primary = 3x impact vs Secondary

**For Cocktails:**
- Taste: sweet, bitter, sour, dry, balanced
- Aroma: fruity, citrus, floral, herbal, savory, spicy, smoky
- Body: refreshing, full-bodied, creamy, effervescent
- Complexity: simple, balanced, complex

**Penalty System:**
- Mismatched taste: -15 points
- Mismatched intensity: -10 points
- Mismatched body: -8 points
- Wrong spirit family: -20 points
- Accumulative penalties for multiple mismatches

**Database Expansion:**
- **735 beverages** comprehensively catalogued
- Complete tasting notes for every drink:
  - Sensory profiles (taste, aroma, mouthfeel)
  - Historical context and origin stories
  - Preparation techniques and variations
  - Serving suggestions and occasions

**Enhanced Descriptions:**
- IBA Cocktails: Origin stories, cultural significance, classic variations
- Spirits: Production methods, regional characteristics, aging notes

**Metadata Expansion:**
- Precise calories counts per serving
- Cost estimation (Low, Medium, High)
- Preparation difficulty (Easy/Medium/Hard)
- Equipment requirements
- Skill level recommendations

**Matching Algorithm Details:**
- Base score calculation from tag matches
- Priority weighting (★=1x, ★★=1.5x, ★★★=2x)
- Penalty application for mismatches
- Score normalization to 0-100 scale
- Classification thresholds validation

**Technical Optimizations:**
- Efficient tag lookup with Map structures
- Memoized scoring calculations
- Lazy evaluation for performance
- Debounced search inputs
- Virtual scrolling for large result sets

---

## Development Statistics (v1.0 → v5.0)

**Database Growth:**
- v1.0: 52 drinks
- v2.0: 120+ drinks
- v3.0: 250+ drinks
- v4.4: 500+ drinks
- v5.0: 700+ drinks

**Feature Evolution:**
- v1.0: Terminal interface, basic BAC
- v2.0: Web interface, fitness parameters
- v3.0: Mobile-first, three sections
- v4.4: Multi-select quiz, priority system
- v4.9: Comparison engine
- v5.0: Detailed matching, complete database

**Code Metrics:**
- Lines of code: ~14,500 (v5.0) (database included)
- Functions: 85+ (v5.0)
- Total development time: ~4 months
- Major refactors: 3 (v3.0, v3.9, v4.7, v5.0)

**Error Reduction:**
- v1.0: ±71% BAC error
- v2.0: ±27% BAC error
- v3.0-v5.0: ±20-25% BAC error (theoretical limit)

---

**Bevi responsabilmente. Non guidare mai dopo aver bevuto alcol.**

*Changelog maintained by Tommaso Merici - December 2025*
