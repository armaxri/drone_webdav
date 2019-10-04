# drone_webdav
This WebDAV plug-in for drone.io allows uploading and downloading files to and from a WebDAV server, as well as other WebDAV operations. This plug-in works with NextCloud and ownCloud server.

## Basic Usage
The plug-in can simply configured and then be executed using commands. Since the plug-in is based on Ubuntu, instead of simple commands also a script can be used to call the functions.

```yaml
pipeline:
  test_plugin:
    image: arnemaxr/drone-webdav:stable
    # To ensure updates and bug fixes:
    pull: true
    webdav_hostname: https://nextcloud.my-server.com
    webdav_root: /remote.php/dav/files/my_test_user
    webdav_login: my_test_user
    webdav_password:
      from_secret: webdav_password
    commands:
      - webdav_mkdir test_dir
      - webdav_list test_dir
      - webdav_upload TestFile.txt test_dir_x/TestFile.txt
      - webdav_download test_dir_x/TestFile.txt TestFile1.txt
      - webdav_copy test_dir_x/TestFile.txt test_dir_z/TestFile.txt
      - webdav_move test_dir_x/TestFile.txt test_dir_y/TestFile.txt
      - webdav_delete test_dir
```

## Available Functions
Since this plug-in is based on Ubuntu, it's possible to use the normal command line calls in the local drone.io repository copy. So functions like "mkdir" and other functions are working. For WebDAV operations the following functions are available.

- **webdav_copy**
    - **First Parameter:** Remote source file or directory.
    - **Second Parameter:** Remote destination for file or directory.
- **webdav_delete**
    - **Parameter:** Remote file or directory which should be deleted.
- **webdav_download**
    - **First Parameter:** Remote source file or directory.
    - **Second Parameter:** Local destination for file or directory.
- **webdav_list**
    - **Parameter:** Remote directory which contend should be printed.
- **webdav_mkdir**
    - **Parameter:** Remote directory which should be created.
- **webdav_move**
    - **First Parameter:** Remote source file or directory.
    - **Second Parameter:** Remote destination for file or directory.
- **webdav_upload**
    - **First Parameter:** Local source file or directory.
    - **Second Parameter:** Remote destination for file or directory.

## NextCloud and ownCloud Specialty
When connecting to a NextCloud or ownCloud server, you have to configure a webdav_root. The root has to look like this "/remote.php/dav/files/***UserName***", where "***UserName***" has to be replaced by the actual user name you use for the connection.

## Connection Options
This plug-in uses [webdav-client-python-3](https://github.com/ezhov-evgeny/webdav-client-python-3), therefor you can use the full feature-set of this powerful module. Use the following parameters in your yaml file to configure the drone.io instance.

```python
        """Constructor of WebDAV client
        :param options: the dictionary of connection options to WebDAV can include proxy server options.
            WebDev settings:
            `webdav_hostname`: url for WebDAV server should contain protocol and ip address or domain name.
                               Example: `https://webdav.server.com`.
            `webdav_login`: (optional) login name for WebDAV server can be empty in case using of token auth.
            `webdav_password`: (optional) password for WebDAV server can be empty in case using of token auth.
            `webdav_token': (optional) token for WebDAV server can be empty in case using of login/password auth.
            `webdav_root`: (optional) root directory of WebDAV server. Defaults is `/`.
            `webdav_cert_path`: (optional) path to certificate.
            `webdav_key_path`: (optional) path to private key.
            `webdav_recv_speed`: (optional) rate limit data download speed in Bytes per second.
                                 Defaults to unlimited speed.
            `webdav_send_speed`: (optional) rate limit data upload speed in Bytes per second.
                                 Defaults to unlimited speed.
            `webdav_verbose`: (optional) set verbose mode on.off. By default verbose mode is off.
            Proxy settings (optional):
             `proxy_hostname`: url to proxy server should contain protocol and ip address or domain name and if needed
                               port. Example: `https://proxy.server.com:8383`.
             `proxy_login`: login name for proxy server.
             `proxy_password`: password for proxy server.
        """
```
