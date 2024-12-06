# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- New functionality added to the project, with reference to issue-ticket (#123)
- Another new item (#1234)

### Fixed
- bugfixes, with references to your issue-tickets (#123)
- another bugfix (#1234)

### Changed
- Changes,  for example code structure
- but also changed/updated dependencies
- Add references to tickets where applicable (#123)

### Removed
- Files that have been removed
- Functionality that has been removed
- Add references to tickets where applicable (#123)


## [0.0.13] - 2024-12-5
### Added
- PR #220 Ppackage-data for Rosim jar files. previous commit was not merged in Omotes-0.5 branch


## [0.0.12] - 2024-12-5
### Fixed
- Issue #216:  Pyjnius should be loaded after initialisation of Ates class to prevent issues with subprocess/forking


## [0.0.11] - 2024-11-8
### Added
- PR #210 Added package-data for Rosim jar files


## [0.0.10] - 2024-11-8
### Added
- Add alpha value from pipe to asset (#205)
- Add port type to assets (#164)
- Documentation for basic controller (#136)
- Added support for more than 2 connectionpoints (#156)

### Changed
- Set priority based on marginal costs (#193)
- Speed improvements, refactored Fluid properties classes (#184)
- Speed improvement by solving heat loss explicitly (#177)
- Speed improvement by solving friction factor explicitly (#178)
- Updated controller to support Ates (#129)

### Fixed
- PR #208 Fixed package build settings 
- Return temperature of Demand cluster not set correctly (#189)


## [0.0.9] - 2024-9-11
### Added
- Ates asset based on Rosim calculations (#97)
- Priority based controller (#128)
- Support for Progress callback from omotes sdk (#144)
- Documentation for the solver (#100)
- Network plot method for debugging (#94)

### Changed
- Updated release workflow (#96)
- Link result-timeseries to ports instead of asset (#114)
- Renamed to omotes-simulator-core
- updated package dependencies

### Fixed
- Many code-style issues
- Unit tests and settings
- Documentation
`

## [0.0.3 - 0.0.8] - 2024-3-24
### Changed
-  Added/tested release workflow in GH actions


## [0.0.2] - 2024-3-24
### Added
- New solver, removing dependency on PandaPipes


## [0.0.1] - 2023-03-16
### Added
- Basic assets: ProductionCluster, DemandCluster, Pipe
- Simulation loop based on PandaPipes
- unit testing
