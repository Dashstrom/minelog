# Logs-Searcher
Script for find somethings easily in your minecraft logs.

## Usage
You can run it with only one argument who is the text to find:
`python3 logs_searcher.py 'hi !'`

You can also use regex using -r or --regex flag:
`python3 logs_searcher.py 'user .* tell something' -r`

Use -p or --path for set the logs path if needed
`python3 logs_searcher.py hi -p /server/logs`

Use -i or --igorecase flag for ignore case !

comand format : `logs_searcher.py [-h] [-p PATH] [-i] [-r] matcher`
