# ESI Routes

This is the routing service for ESI, available at https://esi.evetech.net/ui/?version=_dev#/Routes

This project was initially called eve-pathfinder, and was a collaboration between previous and current CCP developers during Fanfest 2016. The initial plan was to release it as a standalone API, but was not quite finished before work on ESI began.

Since ESI's goal was to provide a framework to create Swagger APIs quickly, it made sense to focus efforts on creating that framework first, then port what was already made into an ESI endpoint.

To this end, all storage (caching), validation, and server boilerplate was removed and replaced with esi-lib.

The ESI framework (esi-lib) is not yet open source. As such, you will not yet be able to actually run this codebase.

The intention of open sourcing this endpoint is not its interactions with esi-lib (which are minimal anyway), but rather because of its standalone nature, and the promise we made to our collaborators. So although you will not be able to fully run this, the hope is that we can work together to make this the best EVE Online routing API possible.
