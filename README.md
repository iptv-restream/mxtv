# mxtv
TV Player for MX

mxtv is a lite version of the [Linux Mint hypnotix player](https://github.com/linuxmint/hypnotix)

__mxtv__

![screnshot](https://github.com/Axel-Erfurt/hypnotixLite/blob/main/screenshot2.png)


__mxtvs__

![screnshot](https://github.com/Axel-Erfurt/hypnotixLite/blob/main/screenshot_s.png)

### Requirements

- python3 >= 3.6
- libmpv1

### Installation

extract it wherever you want

### Start

```cd /path/to/mxtv```

```python3 ./mxtv.py```

### Playlists

Name your lists mychannels[x].txt

[x] from 1 to 9

### Playlist Format

use comma as delimiter, don't use comma in cannel name

```channel name,channel url```

for example

```ARD,http://mcdn.daserste.de/daserste/de/master.m3u8```

or

```my Movie,file:///home/user/Movies/myMovie.mp4```


### Shortcuts

- 1 to 9 -> load list 1 to 9
- f -> toggle Fullscreen
- Escape -> leave Fullscreen
- s -> toggle Sidebar
- wheel -> Zoom in/out
- q -> Quit
- Key Up -> next Channel
- Key Down -> previous Channel
- Key Plus -> more Volume
- Key Minus -> less Volume
- i -> import m3u
- d -> show/hide titlebar
- t -> set window ontop / not ontop

### m3u to mychannels

```python3 m3u_to_channels.py infile.m3u outfile.txt```

- example

```python3 m3u_to_channels.py CA01_CANADA.m3u mychannels4.txt```

### Installer Example

```#!/bin/sh
mkdir ~/Downloads/mxtv-installer
cd ~/Downloads/mxtv-installer
wget https://github.com/Axel-Erfurt/mxtv/archive/refs/heads/main.zip
unzip main.zip
mv mxtv-main mxtv
sudo cp -rf ./mxtv /opt
mxtv_dir=$HOME/.mxtv/
if [ -d "$mxtv_dir" ]
 then
    echo "found $mxtv_dir"
else
    echo "$mxtv_dir not found"
    echo "creating $mxtv_dir"
    mkdir -p $mxtv_dir
    cp ./mxtv/mychannels2.txt ~/.mxtv/mychannels1.txt
fi
cp ./mxtv/mxtv.desktop ~/.local/share/applications
cp ./mxtv/mxtvs.desktop ~/.local/share/applications
rm -rf ~/Downloads/mxtv-installer
```
### Uninstaller Example

```#!/bin/sh
rm -rf ~/mxtv
sudo rm -rf /opt/mxtv
rm ~/.local/share/applications/mxtv.desktop 
rm ~/.local/share/applications/mxtvs.desktop 
```
