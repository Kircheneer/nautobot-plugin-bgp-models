"""Dolt compatibility registration."""

from . import tables

try:
    import dolt  # noqa pylint: disable=unused-import
except ImportError:
    DOLT_AVAILABLE = False
else:
    DOLT_AVAILABLE = True


# Only do this if Dolt is available (aka "version control").
if DOLT_AVAILABLE:

    # Tables used to display diffs
    dolt.register_diff_tables(
        {
            "nautobot_bgp_models": {
                "autonomoussystem": tables.AutonomousSystemTable,
                "peeringrole": tables.PeeringRoleTable,
                "peergroup": tables.PeerGroupTable,
                "peerendpoint": tables.PeerEndpointTable,
                "peersession": tables.PeerSessionTable,
                "addressfamily": tables.AddressFamilyTable,
            }
        }
    )

    # Register all models w/ Dolt.
    dolt.register_versioned_models({"nautobot_bgp_models": True})
