"""
Enable the server's test fixture.

`mass` gives a started server in dev mode with this repository as its local provider folder.
"""

pytest_plugins = ["music_assistant.testing"]
