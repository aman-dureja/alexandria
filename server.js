var express = require('express')
var app = express();
var firebase = require('firebase');
var twilio = require('twilio');
var bodyParser = require('body-parser');
var schedule = require('node-schedule');
var request = require('request');

app.use(bodyParser.urlencoded({extended: false}));

var accountSid = '<SID>';
var authToken = '<AUTH_TOKEN>';

var client = new twilio.RestClient(accountSid, authToken);

app.use(function (req, res, next) {
  console.log('REQUESTS ARE BEING MADE!');
  next();
});

var config = {
    apiKey: "<API_KEY>",
    authDomain: "<AUTH_DOMAIN>",
    databaseURL: "<DATABASE_URL>",
    storageBucket: "<STORAGE_BUCKET>",
    messagingSenderId: "<MESSAGE_SENDER_ID>"
};
firebase.initializeApp(config);

function sendMessage(phoneNumber, body) {
    client.messages.create({
        body: body,
        to: phoneNumber,
        from: '<FROM PHONE NUMBER>'
    }, function(err, message) {
        console.log(err||message);
    });
}

function createNewUser(phoneNumber, book) {
  firebase.database().ref('users').push({
    phoneNumber: phoneNumber,
    book: book,
    curSnippet: 0
  });
  var db = firebase.database();
  var ref = db.ref('phonenumbers');
  ref.push(phoneNumber);
  // send a welcome message
  sendMessage(phoneNumber, 'Welcome to Alexandria. We hope you enjoy it!\nText "help" any time for assistance. Happy reading!');
  // send the first snippet
  firebase.database().ref('users').once('value').then(function(snapshot) {
    var users = snapshot.val();
    for (key in users) {
        if (users[key].phoneNumber === phoneNumber) {
            sendNextSnippet(firebase.database().ref('users/'+key));
            break;
        }
    }
  }).catch(function(err) {
    console.log(err);
  });
}

function sendNextSnippet(userRef) {
    userRef.once('value').then(function(snapshot) {
        var message = '';
        var user = snapshot.val();
        var phoneNumber = user.phoneNumber;
        var curBook = user.book;
        var curSnippet = user.curSnippet;
        var booksRef = firebase.database().ref('books')
        booksRef.once('value').then(function(bookSnapshot) {
            var books = bookSnapshot.val();
            for (key in books) {
                if (books[key].title.toLowerCase() === curBook.toLowerCase()) {
                    var snippetsRef = firebase.database().ref('books/'+key+'/snippets');
                    snippetsRef.once('value').then(function(snippetsSnapshot) {
                        var snippets = snippetsSnapshot.val();
                        if (Object.keys(snippets).length > curSnippet++) {
                            message = snippets[curSnippet];
                            userRef.update({
                                curSnippet: curSnippet
                            });
                        } else {
                            message = 'Congratulations! You have reached the end of the book! To start a new book, just text the title to us!';
                        }
                        sendMessage(phoneNumber, message);
                    }).catch(function(err) {
                        console.log(err);
                    });
                    break;
                }
            }
        }).catch(function(err) {
            console.log(err);
        });
    }).catch(function(err) {
        console.log(err);
    });
}

function parseMessage(phoneNumber, message) {
    if (message.toLowerCase() === 'done') {
        var usersRef = firebase.database().ref('users');
        usersRef.once('value').then(function(snapshot) {
            var users = snapshot.val();
            for (key in users) {
                if (users[key].phoneNumber === phoneNumber) {
                    var userRef = firebase.database().ref('users/'+key);
                    userRef.update({
                        book: 'Unsubscribed',
                        curSnippet: 1
                    });
                    sendMessage(phoneNumber, 'You are now unsubscribed. Text \'assist\' for more info.');
                    break;
                }
            }
        }).catch(function(err) {
            console.log(err);
        });
    } else if (message.toLowerCase() === 'next') {
        var usersRef = firebase.database().ref('users');
        usersRef.once('value').then(function(snapshot) {
            var users = snapshot.val();
            for (key in users) {
                if (users[key].phoneNumber === phoneNumber) {
                    var userRef = firebase.database().ref('users/'+key);
                    sendNextSnippet(userRef);
                }
            }
        }).catch(function(err) {
            console.log(err);
        });
    } else if (message.toLowerCase() === 'what') {
        firebase.database().ref('users').once('value').then(function(snapshot) {
            var users = snapshot.val();
            for (key in users) {
                if (users[key].phoneNumber === phoneNumber) {
                    sendMessage(phoneNumber, 'You are currently reading:\n'+users[key].book);
                }
            }
        }).catch(function(err) {
            console.log(err);
        });
    } else if (message.toLowerCase() === 'assist') {
        var responseMessage = 'assist -- Get a list of available commands\nread <BOOK-NAME> -- Subscribe to a book of your choice\nwhat -- See what book you\'re currently reading\nnext -- Get the next snippet of the book\ndone -- Stop your current subscription'
        sendMessage(phoneNumber, responseMessage);
    } else if (message.toLowerCase().indexOf('dict') != -1) {
        var messageArray = message.toLowerCase().split(' ');
        var word = messageArray[1];

        var baseURL = "http://api.pearson.com/v2/dictionaries/entries?headword=";
        var finalURL = baseURL.concat(word)

        request(finalURL, (error, response, body) => {
            if (!error && response.statusCode === 200) {
                const responseData = JSON.parse(body)
                sendMessage(phoneNumber, responseData["results"][0]["senses"][0]["definition"])
            } else {
                console.log("Got an error: ", error, ", status code: ", response.statusCode)
            }     
        })
    } else if (message.toLowerCase().indexOf('read') != -1) {
        // message is probably a title of a book
        // if the user already exists, we change their book and curSnippet
        // else we create the user with the new book
        var phonesRef = firebase.database().ref('phonenumbers');
        phonesRef.once('value').then(function(snapshot) {
            var phoneNumbers = snapshot.val();
            var userExists = false;
            var messageArray = message.toLowerCase().split(' ');
            var messageBook = messageArray.splice(1, messageArray.length-1).join(' ');
            var bookExists = false;
            for (key in phoneNumbers) {
                if (phoneNumbers[key] === phoneNumber) {
                    userExists = true;
                }
            }
            firebase.database().ref('books').once('value').then(function(snapshot) {
                var books = snapshot.val();
                for (key in books) {
                    if (books[key].title.toLowerCase() === messageBook) {
                        bookExists = true;
                        break;
                    }
                }
                if (bookExists) {
                    if (userExists) {
                        firebase.database().ref('users').once('value').then(function(snapshot) {
                            var users = snapshot.val();
                            for (key in users) {
                                if (users[key].phoneNumber === phoneNumber) {
                                    firebase.database().ref('users/'+key).update({
                                        book: messageBook,
                                        curSnippet: 0
                                    });
                                    sendMessage(phoneNumber, 'You are now subscribed to ' + messageBook + '! Text \'assist\' for help.');
                                    sendNextSnippet(firebase.database().ref('users/'+key));
                                    break;
                                }
                            }
                        }).catch(function(err) {
                            console.log(err);
                        });
                    } else {
                        createNewUser(phoneNumber, messageBook);
                    }
                } else {
                    sendMessage(phoneNumber, 'Sorry, that was either an invalid command or we don\'t have that book in our library. Text "help" any time for assistance!');
                }
            }).catch(function(err) {
                console.log(err);
            });
        }).catch(function(err) {
            console.log(err);
        });
    }
}

function gotPhoneNumber(phoneNumber, message) {
    parseMessage(phoneNumber, message);
}

app.post('/twilio-incoming', function(req, res) {
    gotPhoneNumber(req.body.From, req.body.Body);
});

schedule.scheduleJob('0 0 12 * * *', function(){
  firebase.database().ref('phonenumbers').once('value').then(function(snapshot) {
    var users = snapshot.val();
    for (key in users) {
        gotPhoneNumber(users[key], 'next');
    }
  });
});

app.listen(process.env.port || 8080);
console.log('THINGS ARE HAPPENING!');
