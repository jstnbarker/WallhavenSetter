# WallhavenSetter

See [the API docs](https://wallhaven.cc/help/api#search) for guidance to set up 
custom parameters. Each parameter can be set in the 'payload' key of the 
cofiguration file.

If you prefer a different wallpaper setter, you can change it in the 
`config.json` file as well. Should allow for usage of Wayland compatible setters.

On any changes to the parameter list in the configuration file, you'll need
to force an update with the `--update` flag, otherwise the script will continue to run off
the remaining data until it reaches the end of new wallpapers in that particular 
request.
