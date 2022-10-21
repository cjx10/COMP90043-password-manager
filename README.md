# COMP90043-password-manager
Password manager implementation for COMP90043 research project

# Dependencies
```bash
pip install cryptography
pip install backports.pbkdf2
```

# Usage
`python3 pm.py [operation]`

Operations supported:
[c]reate new password vault, [a]dd new record, [l]ookup record, [g]enerate password, [ag]advanced generate password.

Use `-f` or `--file` flag to specify password vault file location, or default location `./pv` is used. </br>
Use `-h` or `--help` for detailed usage.