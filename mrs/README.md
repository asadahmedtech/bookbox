# BookBox
## API framework for movie booking

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This API framework provides a REST framework for listing, creating and booking shows accross cities.

- List and Filter Theaters according to Movie and City
- Book Seats for show 
- ✨Docker  Enviornment 

## Features

- List Theaters with optional filter parameters of city name and movie name
- List Shows with optional filter parameters of city name, theater name and movie name.
- List all Seats with optional filter parameter of show ID. 
- Book available seats for a show.
- Payment endpoint for verification of transactions.


## Tech

BookBox uses a number of open source projects to work properly:

- [Django] - Backend framework for desiging the services
- [PostgreSQL] - Relational Database 
- [Celery] - Task Queueing Service for booking verifications.
- [Redis] - Broker service for celery
- [Django-Rest-Framework] - Rest framework for Django
- [Docker] - Containerizing

And of course BookBox itself is open source with a [public repository][dill]
 on GitHub.

## Installation

BookBox provides docker images to run the services.

Build the docker image and start the compose file.

```sh
docker-compose build
docker-compose up
```
The serivce will start accepting request at following address.

```sh
0.0.0.0:8000.
``` 

## APIs Available

BookBox is currently providing the following APIs.
Detailed API structure can be found on the OpenAPI Spec Doc .

| TASK | README |
| ------ | ------ |
| List City | [/api/city/?city=<city_id>][red] |
| List Theaters | [/api/theater/?city=<city_name>&movie=<movie_name>][red] |
| List Shows | [/api/show/?city=<city_name>&movie=<movie_name>&theater=<theater_name>][red] |
| List Theater Seats | [/api/show/?theater=<theater_id>][red] |
| List Show Seats | [/booking/seats/?show=<show_id>][red] |
| Book Seats | [/booking/book/][red] |
| List Bookings | [/booking/book/?booking=<booking_id>][red] |
| Payment Confirmation | [/booking/payment/][red] |
| API Documentation | [/redoc/][red] |
| Swagger | [/swagger/][red] |

All the List APIs work using GET requests. Same endpoints can be used for creating new entries by making a POST request with fields of the entry in a JSON body. The body requried for creating new entries of shows, city, theater, seats in a theater and seats in a show can be found in /redoc endpoint.

## Working

#### -- Data Entry
The docker images comes with pre-popoulated data for city, theater, show, seats in a theater and seats in a show. The database schema is provided below. 

![Database Schema](https://github.com/asadahmedtech/bookbox/blob/master/dbschema.png?raw=true)

In order for populating new fields following POST requests are to be made.
1. Add new city:
New City can be added by giving the city name, state and zipcode.
```sh
[POST] /api/city/
```
2. Add new theater:
New theater can be added by giving the exsisting city name, theater name and address.
```sh
[POST] /api/theater/
```
3. Add new theater seats:
New theater seats can be added by giving the exsisting theater id, seatNumber and seatType.
```sh
[POST] /api/theaterseat/
```
4. Add new movie:
New movie can be added by giving the movie name and other optional field like language, certificate, cast, director, image, run_length.
```sh
[POST] /api/movie/
```
5. Add new show:
New show can be added by giving the exsisting movie name, exsisting theater name and datetime for the show.
```sh
[POST] /api/show/
```
6. Add new show seat:
Since every show can have different prices and booking status for the same theater seat a seperate table is created for showseats. It can be created by providing the prices, showID and theater_seatID. It has other parameters of status, bookingID which are populated by internal server calls while booking is initiated.
```sh
[POST] /booking/seat/
```

#### -- Listing of theaters, seats and more
Following set of APIs can be used by the service to show and list down all the movie,  theaters and showtimes in a given city. Each API has its filtering parameters which can be used to narrow down on selection. 
Once a user selects a show to be booked in a theater we will have its showID which will be used in booking APIs.

The docker images comes with pre-popoulated data for city, theater, show, seats in a theater and seats in a show. The query will return following output if called. 

In order for fetching fields following GET requests are to be made.
1. List City:
List of city can be fetched using the API and additional optional parameter of cityID can be provided for fetching a particular city.
```sh
[GET] /api/city/
[RESPONSE] HTTP 200 OK
Content-Type: application/json
Vary: Accept
[
    {
        "id": 1,
        "city": "HYDERABAD",
        "state": "Telangana",
        "zipcode": 506004
    },
    {
        "id": 2,
        "city": "DELHI",
        "state": "Delhi",
        "zipcode": 406001
    }
]
```
2. List Theater:
List of theater can be fetched using the API and additional optional parameter of city name can be provided for fetching a particular city, movie name for fetching for a particular movie can be provided.
```sh
[GET] /api/theater/
[RESPONSE] HTTP 200 OK
Content-Type: application/json
Vary: Accept
[
    {
        "id": 1,
        "city": {
            "id": 1,
            "city": "HYDERABAD",
            "state": "Telangana",
            "zipcode": 506004
        },
        "name": "SPI S2",
        "address": "Gachibowli"
    },
    {
        "id": 2,
        "city": {
            "id": 1,
            "city": "HYDERABAD",
            "state": "Telangana",
            "zipcode": 506004
        },
        "name": "PVR",
        "address": "Hitech City"
    },
    {
        "id": 3,
        "city": {
            "id": 1,
            "city": "HYDERABAD",
            "state": "Telangana",
            "zipcode": 506004
        },
        "name": "INOX",
        "address": "Hitech City"
    },
    {
        "id": 4,
        "city": {
            "id": 2,
            "city": "DELHI",
            "state": "Delhi",
            "zipcode": 406001
        },
        "name": "PVR",
        "address": "Delhi"
    },
    {
        "id": 5,
        "city": {
            "id": 2,
            "city": "DELHI",
            "state": "Delhi",
            "zipcode": 406001
        },
        "name": "IMAX",
        "address": "Chruch Street"
    }
]
```
Filter query with city name and movie name.
```sh
[GET] /api/theater/?city=DELHI&movie=Avengers
[RESPONSE] HTTP 200 OK
Content-Type: application/json
Vary: Accept
[
    {
        "id": 4,
        "city": {
            "id": 2,
            "city": "DELHI",
            "state": "Delhi",
            "zipcode": 406001
        },
        "name": "PVR",
        "address": "Delhi"
    }
]
```
It returns empty JSON response if any of the query parameters is not present.
3. List movies:
List of movies in the database can be fetched using the API
```sh
[GET] /api/movie/
[RESPONSE] HTTP 200 OK
Content-Type: application/json
Vary: Accept
[
    {
        "id": 1,
        "name": "Avengers",
        "cast": "",
        "director": "",
        "language": "ENGLISH",
        "run_length": null,
        "certificate": "A",
        "image": null
    },
    {
        "id": 2,
        "name": "Stuart Litte",
        "cast": "",
        "director": "",
        "language": "ENGLISH",
        "run_length": null,
        "certificate": "A",
        "image": null
    },
]
```
4. List Shows:
Shows are listed when a theater is screeing a movie at different times, the shows can be fetched using the API and optional parameters of cityname, theatername or moviename can be provided for filtering for a particulars show.
```sh
[GET] /api/show/?city=DELHI
[RESPONSE] HTTP 200 OK
Content-Type: application/json
Vary: Accept
[
    {
        "id": 6,
        "theater": {
            "id": 4,
            "city": {
                "id": 2,
                "city": "DELHI",
                "state": "Delhi",
                "zipcode": 406001
            },
            "name": "PVR",
            "address": "Delhi"
        },
        "movie": {
            "id": 1,
            "name": "Avengers",
            "cast": "",
            "director": "",
            "language": "ENGLISH",
            "run_length": null,
            "certificate": "A",
            "image": null
        },
        "show_time": "2021-04-12T17:00:00Z"
    },
]
```

#### -- Booking of shows and Payment
Following set of APIs can be used by the service to book seats in a given show user has selected. The fetch apis can be used to get the current status of seats accross a given show and book them using the API.
The showID selected by the user is being used here.
1. List Seats in a show:
This API will list all the seats available in a selected show. Each seat has its ID and status. Status of True means the seat is either booked or temporarily occupied. FrontEnd can fetch the seating map from the database and use the seatID provided for displaying a seating arrangement.
User can select the seats which status are false and provide the list of showseatID to the booking API.
```sh
[GET] /booking/seat/?showID=6
[RESPONSE] HTTP 200 OK
Content-Type: application/json
Vary: Accept
[
    {
        "id": 1,
        "price": 100.0,
        "status": true,
        "seat": 1,
        "show": 6,
        "booking": null
    },
    {
        "id": 5,
        "price": 150.0,
        "status": false,
        "seat": 5,
        "show": 6,
        "booking": null
    },
    {
        "id": 6,
        "price": 150.0,
        "status": false,
        "seat": 6,
        "show": 6,
        "booking": null
    },
    {
        "id": 7,
        "price": 150.0,
        "status": false,
        "seat": 6,
        "show": 6,
        "booking": null
    },
]
```
2. Book Seats in a show:
This API will book the selected seats available in a selected show. The seats selected by the user are passed as an array to the bookingAPI along with user details and show details. When the backend service recives the request it checks for the seat availablity, if all the seats are available then an atomic transaction is made and seats are temperorily booked. A Booking object is created with the user details and a subsequent payment object is created for payment details. Payment object and All the seats booked are updated with BookingID as per the schema. 
User gets 15minutes to make the payment, if no payment is made the seats are automatically unreserved after 15minutes. This is achieved using shared task in celery.
```sh
[POST] /booking/book/
--- [BODY] {
    "showID":6,
    "user": "asad",
    "seats": [6, 7]
}
[RESPONSE] 
    {
    "id": 35,
    "show": {
        "id": 6,
        "theater": {
            "id": 4,
            "city": {
                "id": 2,
                "city": "DELHI",
                "state": "Delhi",
                "zipcode": 406001
            },
            "name": "PVR",
            "address": "Delhi"
        },
        "movie": {
            "id": 1,
            "name": "Avengers",
            "cast": "",
            "director": "",
            "language": "ENGLISH",
            "run_length": null,
            "certificate": "A",
            "image": null
        },
        "show_time": "2021-04-12T17:00:00Z"
    },
    "status": "PROG",
    "user": "asad",
    "created_at": "2021-04-14T11:06:18.291819Z"
}
```
2. Payment of seats:
This API will confirm the booking by changing the booking status to SUCC. If the payment is successfull. It is a redirection API which will be called by payment gateway on reciving confimation of transaction. If the transaction is success the seats are permanantly booked for the show. If the transaction is a failure seats are unreserved immediately.
User gets 15minutes to make the payment, if no payment is made the seats are automatically unreserved after 15minutes. This is achieved using shared task in celery. If payment is recieved after 15minutes then the gateway returns a response of payment timeout and the money has to be refunded.
```sh
[POST] /booking/payment/
--- [BODY] {
    "paymentID": 24,
    "status": "Success",
    "transactionID": "123456789"
}
[RESPONSE] {
    "id": 24,
    "amount": 300.0,
    "transactionID": "123456789",
    "discountID": "",
    "created_at": "2021-04-14T11:06:18.291819Z",
    "paymentMethod": "",
    "booking": 35
}
```
As the payment was made is a success the status of the booking can be fetched and it will return a status of SUCC. If the payment was failed the status will change to FAIL from PROG.
```sh
[GET] /booking/book/?bookingID=35
[RESPONSE] HTTP 200 OK
Content-Type: application/json
Vary: Accept
[
    {
        "id": 35,
        "show": {
            "id": 6,
            "theater": {
                "id": 4,
                "city": {
                    "id": 2,
                    "city": "DELHI",
                    "state": "Delhi",
                    "zipcode": 406001
                },
                "name": "PVR",
                "address": "Delhi"
            },
            "movie": {
                "id": 1,
                "name": "Avengers",
                "cast": "",
                "director": "",
                "language": "ENGLISH",
                "run_length": null,
                "certificate": "A",
                "image": null
            },
            "show_time": "2021-04-12T17:00:00Z"
        },
        "status": "SUCC",
        "user": "asad",
        "created_at": "2021-04-14T11:06:18.291819Z"
    }
]
}
```

## Future Scope
#### Authentication
Each REST API can have a bearer JWT token which can be used to secure all the endpoints. JWT Token can be generated once the users login into the website. The token can be validated everytime an API endpoint is fetched using middlewears. While booking instead of providing explicitly about the user, data can be fetched from the Token details.
#### Logging and Messaging Queues
LogStash and Kafka can be used for logging and messaging purposes. Once a user has confirmed the booking kafka can be used to send SMTP responses about the tickets to their mails or any push notification service.
#### NoSQL Database
Currently the movie information is being stored in a SQL database, which can contain a lot of data if we plan to incorporate user ratings, comments and reviews. Such data can be stored in a NoSQL database for faster access. 

## License

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/asadahmedtech/bookbox>
   [django]: <https://www.djangoproject.com/>
   [postgresql]: <https://www.postgresql.org/>
   [celery]: <https://docs.celeryproject.org/en/stable/>
   [redis]: <https://redis.io/>
   [django-rest-framework]: <https://www.django-rest-framework.org/>
   [docker]: <https://www.docker.com/>

   [red]: <https://github.com/asadahmedtech/bookbox/tree/master/README.md>
