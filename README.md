# asciiforge

**[try it in your browser](https://masterxhackerx420-oss.github.io/asciiforge/)**, no install needed.

Type a sentence, get it back as ASCII text art in the style you pick.

```
$ asciiforge "make art" -f slant
                    __                      __ 
   ____ ___  ____ _/ /_____     ____ ______/ /_
  / __ `__ \/ __ `/ //_/ _ \   / __ `/ ___/ __/
 / / / / / / /_/ / ,< /  __/  / /_/ / /  / /_  
/_/ /_/ /_/\__,_/_/|_|\___/   \__,_/_/   \__/  
                                               
```

## Install

```bash
pip install git+https://github.com/masterxhackerx420-oss/asciiforge
```

Needs Python 3.9+. The only dependency is [pyfiglet](https://github.com/pwaller/pyfiglet).

## Run

```bash
asciiforge "hello world"              # default font (standard)
asciiforge "hello world" -f doom      # pick a style (any pyfiglet font name works)
asciiforge --list                     # curated styles
asciiforge --all "hi"                 # preview in every curated style
asciiforge "a long sentence" --width 60   # wrap to 60 columns (default: terminal width)
asciiforge "boxed" --border -o art.txt    # draw a box and save to a file
echo "piped in" | asciiforge -f small     # read from stdin
```

## Develop

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e . pytest
pytest
```

## License

MIT
