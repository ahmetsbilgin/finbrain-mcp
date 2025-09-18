from finbrain_mcp.tools import health as mod


def test_health_ok(patch_resolvers):
    # Reuse your fixture from conftest.py to patch resolve_api_key + FBClient
    patch_resolvers(mod)

    out = mod.health()
    assert out["ok"] is True
    assert isinstance(out.get("mcp_version"), str)
    assert "sdk" in out and out["sdk"]["package"] == "finbrain-python"
