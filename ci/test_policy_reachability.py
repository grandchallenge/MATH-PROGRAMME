#!/usr/bin/env python3
"""Adversarial tests for executable CI policy reachability."""
from __future__ import annotations

import tempfile
from pathlib import Path

from validate_policy_reachability import policy_reachability_errors

WORKFLOW = """name: Synthetic policy
on: [pull_request]
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - run: python3 ci/root_check.py
"""


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / "ci").mkdir()
        (root / ".github" / "workflows" / "ci.yml").write_text(WORKFLOW, encoding="utf-8")
        (root / "ci" / "campaign_replay_registry.json").write_text(
            '{"entries": []}\n', encoding="utf-8"
        )
        (root / "ci" / "root_check.py").write_text(
            "#!/usr/bin/env python3\nfrom helper_check import run\nif __name__ == '__main__':\n    run()\n",
            encoding="utf-8",
        )
        (root / "ci" / "helper_check.py").write_text(
            "def run():\n    return None\n",
            encoding="utf-8",
        )
        assert not policy_reachability_errors(root)

        rogue = root / "ci" / "rogue_check.py"
        rogue.write_text(
            "#!/usr/bin/env python3\nif __name__ == '__main__':\n    print('rogue')\n",
            encoding="utf-8",
        )
        assert any(
            "rogue_check.py" in error and "unreachable" in error
            for error in policy_reachability_errors(root)
        )

        (root / "ci" / "root_check.py").write_text(
            "#!/usr/bin/env python3\nfrom helper_check import run\nfrom rogue_check import main\n"
            "if __name__ == '__main__':\n    run()\n    main()\n",
            encoding="utf-8",
        )
        rogue.write_text(
            "def main():\n    print('reachable')\n\nif __name__ == '__main__':\n    main()\n",
            encoding="utf-8",
        )
        assert not policy_reachability_errors(root)

        (root / ".github" / "workflows" / "ci.yml").write_text(
            WORKFLOW.replace("ci/root_check.py", "ci/missing.py"), encoding="utf-8"
        )
        assert any(
            "missing Python script ci/missing.py" in error
            for error in policy_reachability_errors(root)
        )

        (root / ".github" / "workflows" / "ci.yml").write_text(WORKFLOW, encoding="utf-8")
        (root / "governance").mkdir()
        (root / "governance" / "gcl_tooling_command_contract.json").write_text(
            "{}\n", encoding="utf-8"
        )
        assert any(
            "incomplete tooling control surface" in error
            and "ci/gcl.py" in error
            and "schemas/gcl_tooling_command_contract.schema.json" in error
            for error in policy_reachability_errors(root)
        )

        (root / "governance" / "gcl_tooling_command_contract.json").unlink()
        (root / "negative_knowledge").mkdir()
        (root / "negative_knowledge" / "pilot_registry.json").write_text(
            "{}\n", encoding="utf-8"
        )
        assert any(
            "incomplete control surface" in error
            and "ci/validate_negative_knowledge.py" in error
            and "schemas/negative_knowledge_registry.schema.json" in error
            for error in policy_reachability_errors(root)
        )

    print("CI policy reachability rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
