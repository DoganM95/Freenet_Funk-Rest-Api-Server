# Freenet Funk Rest Api Server

Runs a flask (python) server which takes HTTP requests to get your data from Funk servers or order a specific mobile plan for the following day.

## Getting Started

pull the image using `docker pull doganm95/freenet_funk-rest-api-server:latest`

### Usage

For a usage manual (structure of requests, etc), [click here](https://github.com/DoganM95/Freenet_Funk-rest-api-server#requests)

#### Container Parameters

`-p <port>:5000`  
`-e "FUNK_USERNAME=<your_username>"`  
`-e "FUNK_PASSWORD=<your_password>"`  
`-e "PASSWORD_HASHING_ALGORITHM=<your_preferred_algorithm"`  
`-e "SSL_PRIVATE_KEY=<your_server_ssel_private_key>"`  
`-e "SSL_CERT=<your_server_ssl_cert>"`  
`-e "SERVER_MODE=<mode>"`  
`-v "<your_local_pem_certs_folder>:/usr/src/app/volume/ssl/"`  
  
#### Example commands to run the image

```shell
docker run \
-p 8080:5000 \
-e "FUNK_USERNAME=someone@gmail.com" \
-e "FUNK_PASSWORD=passW"  \
-e "PASSWORD_HASHING_ALGORITHM=sha512" \
-e "SERVER_MODE=prod" \
-v "C:\Users\Dogan\OneDrive\Desktop\certs_tmp\:/usr/src/app/volume/ssl/" \
doganm95/freenet_funk-rest-api-server
```

```shell
docker run \
-p 8080:5000 \
-e "FUNK_USERNAME=someone@gmail.com" \
-e "FUNK_PASSWORD=passW"  \
-e "PASSWORD_HASHING_ALGORITHM=sha512" \
-e "SERVER_MODE=prod" \
"SSL_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----  
    000000000000000000000000000000000000000000000000000000  
    000000000000000000000000000000000000000000000000000000
    ...
    -----END RSA PRIVATE KEY-----
" \
    -e "SSL_CERT==-----BEGIN CERTIFICATE-----  
    000000000000000000000000000000000000000000000000000000  
    000000000000000000000000000000000000000000000000000000
    ...
    -----END CERTIFICATE-----
" \
doganm95/freenet_funk-rest-api-server
```

#### Environment Variables

- `FUNK_USERNAME` - Your Freenet Funk username, usually an email address
- `FUNK_PASSWORD` - Your Freenet Funk password
- `PASSWORD_HASHING_ALGORITHM` - supported:  
    `md4, sm3, blake2b, sha256, sha1, sha3_256, sha512, shake_128, ripemd160, sha3_384, whirlpool, md5-sha1, sha384, sha512_224, blake2s ,sha3_224, md5, shake_256, sha512_256, sha224, sha3_512`.  
    Default, if omitted: `sha3_512`
- `SSL_PRIVATE_KEY` and  `SSL_CERT` are just the contents of the .pem files. Messing with the new lines is not recommended and can lead to unexpected behavior.  
Omit, if volume should be used to store .pem files instead. Correct anonymized example:

    ```shell
    "SSL_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----  
    000000000000000000000000000000000000000000000000000000  
    000000000000000000000000000000000000000000000000000000
    ...
    -----END RSA PRIVATE KEY-----
    " \
    -e "SSL_CERT=..."
    ```

- `SERVER_MODE` can be `prod` or `dev`. For initial container setup & testing, try dev. If everything works, you can switch to `-e "SERVER_MODE=prod"`, to turn off console logs

#### Volumes
- `<local_cert_folder>:/usr/src/app/volume/ssl/` - can contain the cert.pem and privkey.pem as files, if the docker run args are not working (e.g. on a Synology NAS).  
In that case, just omit the `-e "SSL_PRIVATE_KEY=..." -e "SSL_CERT=..."` and use this `-v ...` instead.
