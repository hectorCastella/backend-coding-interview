# Clever's Backend Engineering Challenge

## Tools use
- Docker
- Django
- Postgresql as default database

## API design
There are two main apps in this project
account and photo.

## Commands
This project use docker. therefore it is required to have that install. then execute the following commands

```
docker compose up
```

in a different terminal execute the following commands
```
docker exec -it clever-assignment-app /bin/bash

python manage.py migrate
```

### Models
- Photographer: is a photographer instance, it has an external id and name. It represent the photographer.
- Photo: It represent the photo that want to be upload. It is importnat to notify that the original photo required a URL, and some unique paramater different to photo variants
- PhotoVariant: It is possible that a photo has multiple variants, in this case the sizes is the mean attribute.

### URL

#### Create an account
URL: */auth/signup*

METHOD: *POST*

Body
```
{
  "username": "new_user_name",
  "email": "new_user_email",
  "password": "password_of_new_user"
}
```
---
#### Logn in
URL: */auth/login*

METHOD: *POST*

Body
```
{
  "username" : username create,
  "password" : password
}
```
---
#### Upload all the photos
URL: */photos/upload-data*

METHOD: *POST*

HEADERS: "Authorization": "Token {Token}

Body
ensure you using multipart form
```
  {
    "file": file
  }
```
---
#### Get all Photos
URL: */photos/photos*

METHOD: *GET*

HEADERS: "Authorization": "Token {Token}

Body
```
[
  {
    "id": "photo id",
    "photographer" : {
      "id": int,
      "external_id": int,
      "name": string,
      "url": string,
    },
    "photos_variants": [
      {
        "id": int,
        "variant_name": string,
        "url": string
      }
      ...
    ],
    "external_id": int,
    "width": int,
    "height": int,
    "url": string,
    "avg_color": string,
    "alt": string
  }
]
```
---
#### Photogher
URLs: */photos/photographer*,*/photos/photographer/{id}* 

METHOD: *GET/POST/PATCH*

HEADERS: "Authorization": "Token {Token}

Body
required to specify an photographer to create or update
```
{
  "external_id" : int,
  "name" : string,
  "url": string
}
```
---
#### Photos 
URLs: */photos/photos*,*/photos/photos/{id}* 

METHOD: *GET/POST/PATCH*

HEADERS: "Authorization": "Token {Token}

Body
required to specify an photographer to create a photo.
variants is optional and need to pass here to create a new one
```
{
  "id": "photo id",
  "photographer" : {
    "id": int,
    "external_id": int,
    "name": string,
    "url": string,
  },
  "photos_variants": [
    {
      "id": int,
      "variant_name": string,
      "url": string
    }
    ...
  ],
  "external_id": int,
  "width": int,
  "height": int,
  "url": string,
  "avg_color": string,
  "alt": string
}
```
---
#### Photos Variants
URLs: */photos/photos-variants*,*/photos/photos-variants/{id}* 

METHOD: *GET/POST/PATCH*

HEADERS: "Authorization": "Token {Token}

Body
```
{
  "id": int,
  "variant_name": string,
  "url": string
}
```
---