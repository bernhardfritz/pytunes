# pytunes

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

## How does it work?

pytunes analyzes [ID3](https://en.wikipedia.org/wiki/ID3) metadata of your MP3 files and generates [M3U](https://en.wikipedia.org/wiki/M3U) playlists so you can stream your music with an [HLS](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)-compatible media player over the internet.

## Instructions

- Set up your Raspberry Pi device with balenaOS in **production mode** and bring it online on the balenaCloud dashboard by following the [getting started guide](https://docs.balena.io/learn/getting-started/).
- Open a terminal on your local computer and type:

  ```bash
  # clone repository
  git clone https://github.com/bernhardfritz/pytunes.git

  # change directory
  cd pytunes

  # generate database password
  cp .env.template .env && echo "$(date | md5sum | head -c 32)" >> .env

  # register first user
  htpasswd -c .htpasswd <username>

  # register another user
  # htpasswd .htpasswd <another username>

  # deploy to balenaCloud
  balena push <fleet name>
  ```

- Please be patient. It might take a couple of minutes until deployment is complete.
- You should see a log line in your balenaCloud dashboard once pytunes has started successfully:
  ```
  INFO:     Application startup complete.
  ```
- Add your public SSH key to balenaCloud by following the [SSH access guide](https://docs.balena.io/learn/manage/ssh-access/#add-an-ssh-key-to-balenacloud).
- Determine your `balena-username` by typing:
  ```bash
  balena whoami
  ```
- Determine your `APP ID` by typing:
  ```bash
  balena fleet <fleet name> --fields=id
  ```
- Copy an MP3 file from your local computer to your Raspberry Pi (`short-uuid` refers to the first 7 characters of your `BALENA_DEVICE_UUID`):
  ```bash
  scp -P 22222 track.mp3 <balena-username>@<short-uuid>.local:/var/lib/docker/volumes/<APP ID>_pytunes-data/_data/
  ```
  Alternatively you can also use an SFTP client of your choice like [FileZilla](https://filezilla-project.org/).
- pytunes will automatically start processing MP3 files as soon as they have been received.
- You should see a log line in your balenaCloud dashboard once an MP3 file has been processed successfully:
  ```
  21:01:35 default: Job OK (a9e5765b-f1f8-4dc6-8ecd-166a2e21f6d1)
  ```
- Expose your Raspberry Pi to the internet by switching on [public device URL](https://docs.balena.io/learn/manage/actions/#public-device-url).
- Install an HLS-compatible media player of your choice like [VLC](https://www.videolan.org/vlc/):

  [![Windows](windows.png)](https://www.videolan.org/vlc/download-windows.html)
  [![macOS](macos.png)](https://www.videolan.org/vlc/download-macosx.html)
  [![Linux](linux.png)](https://www.videolan.org/vlc/#download)
  [![Android](android.png)](https://www.videolan.org/vlc/download-android.html)
  [![iOS](ios.png)](https://www.videolan.org/vlc/download-ios.html)

- Open network stream in VLC:
  ```
  https://<username>:<password>@<BALENA_DEVICE_UUID>.balena-devices.com/
  ```
- Enjoy!

## License

MIT
