### Limitations
Requires enviornment var with the name of 'MAL_KEY' with your api key as the value

Currently goes through the entire year of 2016 downloading PE32 files

### TODO
* Add different filetypes
* Add ability to change date
* Check to see if the hash currenlt exists in the CWD to save API requests
* Add a shuffle feature so file downloading is not always sequential.
  * In addition, add a check to stop trying to download once ratelimit is hit. Files are created with their content being the API rate limiting error message.
  * In conjunction with the above feature, the script should also check locally to see if the hash exists before attempting to even check if it is a PE32 file. This will save additional API requests when the script is run multiple times on the same directory.
* Have the dry_run functionality print out how many samples would be downloaded
