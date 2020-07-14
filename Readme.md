
<p align="center"> 
<img src="https://github.com/karimelgazar/cv-with-things/raw/master/images/islamic.png" style="float: left" width=15%/>

<img src="https://github.com/karimelgazar/cv-with-things/raw/master/images/b0.png" style="float: center" width=50%/>

<img src="https://github.com/karimelgazar/cv-with-things/raw/master/images/islamic.png" style="float: right" width=15%/>
</p>

<br>

# Youtube Downloader for the blind 👨‍🦯 and the sighted 🚶 
Download Any Link whether a single video, a playlist, or a whole channel Using Internet Download Manger
## The Index
[**NVDA Addon (For the blind)**](#nvda-addon-) &nbsp;**|**&nbsp;
[**Terminal Version (for the sighted)**](#terminal-version-) &nbsp;**|**&nbsp;
[**Settings File**](#settings-file-) &nbsp;**|**&nbsp;
[**Special Thanks**](#special-thanks-)

## NVDA Addon 👨‍🦯
🌟 You can download the addon from [this direct link](https://github.com/karimelgazar/youtube-downloader/releases/download/1.0.0/windows-youtubeDownloder-1.0.0.nvda-addon) <br>

🌟 The addon has `3 shortcuts`: <br>
1. `alt+control+y` : "To Start Downloading The Seleceted Link"
2. `alt+control+r` : "To Rename Non English Videos Titles To Its Orignal Ones After Downloadding",
3. `alt+control+l` : "To Configure The Addon Settings",` 

💁 How To Use:
1. Choose the link you want to download whether a single video, a playlist, or a whole channel <br>
    ⚠ The channel url must ends with "/videos" 
    so you need to select the videos tab in the channel page and then copy the url
    
    ⚠ If you downloaded a single video it will be inside a folder this folder name 
    is the same as the original video title and same for channels or playlists
2. Press `ctrl+l` then `alt+control+y` and the download will begin in IDM <br>
    ⚠ The addon will beign downloading depending on the default settings unless you change it [please see this](#settings-file-) 

3. The addon can't name non-english vidos with their original names due to some limitation
on windows so after downloading your non-english titled videos you need to press the shortcut
`alt+control+r` and select the video or playlist or channel `folder` to rename the videos
inside this folder with its original names

## Terminal Version 🚶

🌟 You need to download the repo from [here](https://github.com/karimelgazar/youtube-downloader/archive/master.zip)

🌟 All what you need is inside the folder [`main_youtube_downloader`](./main_youtube_downloader)

💁 How To Use:
1. You copy the link to download then pass it to the `main_youtube_downloader/original_script.py` in the terminal 

    ⚠ The channel url must ends with "/videos" 
    so you need to select the videos tab in the channel page and then copy the url
    
    ⚠ If you downloaded a single video it will be inside a folder this folder name 
    is the same as the original video title and same for channels or playlists

2. The script will beign downloading depending on the default settings unless you change it [please see this](#settings-file-) 

3. The addon can't name non-english vidos with their original names due to some limitation
on windows so after downloading your non-english titled videos you need to run `main_youtube_downloader/terminal_vidoes_renamer.py` and select the video or playlist or channel `folder` to rename the videos inside this folder with its original names

## Settings File 📑
🌟 This is a txt file that contains user configuration purpose of each line in the file (in order) as follows: 

1. The path to the idman.exe file
    ⚠ in future uptdates new dowloaders will be added like `Uget`
2. The path where all downloads will be saved to.
3. If you want to download in video format <br>
    ⚠ `True` OR `False` use the word with the same punctuation
4. The quality of the video you want to download <br>
    ⚠ Choose From:`144p`, `240p`, `360p`, `480p`, `720p` use the word with the same punctuation

🌟 If you use `NVDA Addon` 👨‍🦯:
press the shortcut `alt+control+l` and you will have a windows to set the info above

🌟 If you use the `Terminal Version` 🚶:
run the script `main_youtube_downloader/terminal_configure_settings.py` and you will set the info above in the terminal

## Special Thanks 🤝
Thanks to [eng. Wafiq Taher](https://github.com/wafiqtaher) for helping me in cofiguring the scripts with NVDA
