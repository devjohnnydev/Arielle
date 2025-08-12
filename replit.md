# Church T-Shirt Order Management System

## Overview

This is a Flask-based web application designed to help Arielle Tigre, the administrator of Assembleia de Deus Comadesha Jerusalém, manage t-shirt orders and payments for the church congress. The system provides a comprehensive solution for tracking orders, managing payments, and generating reports with an intuitive interface that reflects the church's official visual identity based on their logo.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
The application is built using Flask, a lightweight Python web framework that provides flexibility and simplicity for rapid development. Flask was chosen for its minimal setup requirements and excellent documentation, making it ideal for small to medium-sized applications.

**Key Components:**
- **Flask-SQLAlchemy**: ORM for database operations, providing an abstraction layer that simplifies database interactions
- **Flask-WTF**: Form handling and CSRF protection, ensuring secure form submissions
- **Werkzeug**: Password hashing and security utilities for admin authentication
- **Session-based authentication**: Simple session management without complex user roles

### Database Design
The system uses SQLAlchemy with a flexible database configuration that defaults to SQLite for development but can be easily switched to PostgreSQL or other databases via environment variables.

**Core Models:**
- **Admin Model**: Simple authentication for the single administrator (Arielle)
- **Order Model**: Comprehensive order tracking including congregation, size, quantity, pricing, payment status, and audit timestamps
- **Automatic calculations**: Total amounts are calculated automatically based on quantity and unit price

### Frontend Architecture
The frontend uses a traditional server-side rendering approach with Jinja2 templates, chosen for simplicity and reduced complexity compared to separate frontend frameworks.

**UI Framework:**
- **Bootstrap 5**: Responsive design framework ensuring mobile compatibility
- **Font Awesome**: Icon library for enhanced visual communication
- **Chart.js**: Interactive charts for dashboard analytics
- **Custom CSS**: Church-branded color scheme and styling

### Application Structure
The application follows a modular Flask pattern with clear separation of concerns:

**Core Modules:**
- `app.py`: Application factory and configuration
- `models.py`: Database models and business logic
- `routes.py`: HTTP endpoints and request handling
- `forms.py`: Form definitions and validation rules
- `utils.py`: Helper functions including authentication decorators and data export utilities

### Security Implementation
Security is implemented through multiple layers:
- **Password hashing**: Using Werkzeug's secure password hashing
- **Session management**: Flask's built-in session handling with secret keys
- **Form protection**: CSRF tokens via Flask-WTF
- **Input validation**: Server-side validation for all form inputs

### Data Management Features
The system provides comprehensive data management capabilities:
- **CRUD operations**: Full create, read, update, delete functionality for orders
- **Advanced filtering**: Multi-criteria filtering for orders by congregation, size, payment status
- **Export functionality**: CSV export capability for reporting and external analysis
- **Audit trails**: Created and updated timestamps for all orders

## External Dependencies

### Core Python Packages
- **Flask**: Web framework for HTTP handling and routing
- **Flask-SQLAlchemy**: Database ORM and connection management
- **Flask-WTF**: Form handling and security features
- **Werkzeug**: Password hashing and WSGI utilities

### Frontend Libraries (CDN)
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome 6**: Icon library for user interface elements
- **Chart.js**: JavaScript charting library for dashboard analytics

### Development Dependencies
- **SQLite**: Default database for development and testing
- **Python 3.x**: Runtime environment

### Production Considerations
- **PostgreSQL**: Recommended production database (configurable via DATABASE_URL environment variable)
- **Gunicorn**: WSGI server for production deployment
- **Environment variables**: Configuration management for sensitive data like database URLs and session secrets

### Church-Specific Integrations
- **Instagram**: Social media integration link to @ieadajerusalem
- **Church branding**: Updated visual identity based on official church logo with blue, gold, and white color scheme
- **Logo**: Custom SVG logo featuring the church's official design elements (Assembleia de Deus, Comadesha, Jerusalém)
- **Portuguese localization**: All interface elements in Portuguese for the Brazilian church context
- **Sample data**: Functionality to load example congregation data for testing and demonstration purposes

## Recent Updates (August 2025)

### Visual Identity Overhaul
- Updated color palette based on official church logo:
  - Primary: Deep blue (#1e3a8a)
  - Secondary: Blue (#3b82f6) 
  - Accent: Gold/Yellow (#fbbf24)
  - Supporting: Gold (#d97706)
- Created new SVG logo reflecting church's actual branding with circular design, wheat decorations, and proper church name
- Updated all templates and styles to use new church name "Assembleia de Deus Comadesha Jerusalém"

### Enhanced Functionality
- Added sample data loading feature with realistic congregation names and order data
- Improved error handling in authentication flow
- Enhanced dashboard with conditional display of sample data loading option

### Excel-Based Data Integration (August 12, 2025)
- Integrated actual Excel spreadsheet data structure for comprehensive batch management
- Updated batch system with 7 complete lotes:
  - 1º LOTE, 2º LOTE (standard batches)
  - 3º LOTE (10/05), 4º LOTE (25/05) (with specific dates)
  - 5º LOTE (10/06), 6º LOTE (25/06), 7º LOTE (10/08) (complete date management)
- Database schema enhanced with:
  - batch_number field with all 7 lote options
  - batch_date field for individual lote date tracking
  - delivery_date field for delivery management
  - Expanded size options: PP, P, M, G, GG, EXTG, 2 anos, 6 anos, 8 anos, 9 anos, 10 anos, 1 ANO
- Sample data updated with real congregations from Excel:
  - Over 50 authentic congregation names from actual church data
  - Realistic quantity distributions matching Excel patterns
  - Accurate batch assignments reflecting actual workflow
- Dynamic filtering system enhanced:
  - Batch filtering with all 7 lotes
  - Congregation filtering with real church names
  - Size and payment status filtering
  - Date range filtering for comprehensive reporting
- UI improvements for batch management:
  - Updated forms with complete lote options
  - Enhanced tables showing batch dates and delivery tracking
  - Improved badge styling for batch identification
  - Streamlined filtering interface for efficient data management