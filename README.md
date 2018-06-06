# Moon Phases Dashboard
🌒🌒🌓🌔🌕🌖🌗🌘🌑 Command-line tool that scrapes data from timeanddate.com 

![the less eye strain version](https://imgur.com/5RVFy0P "In use")
![output with gradient](https://imgur.com/sJhroTe "Piped to lolcat")

## Usage
You can run it in a shell by supplying it with the country and city name you'd like to use: 
```
$ ./astro.py canada montreal
```
Run `python3 -m pip install --user -r requirements.txt` to install all dependencies. Uses Python 3.5.2

It uses beautifulsoup to scrape from timeanddate.com, and a little regex to parse. The unicode moon phases are displayed assuming you're running a terminal with a black background. 
