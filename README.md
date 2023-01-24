# Autocomplete API Project

```
* Install redis-server and run on port 6379
* pip install -r requirements.txt
* run main.py
```

# Redis
```
    current implementation uses redis sorted set as Datastructure to store count of prefixes to get autocomplete words
```

# API
``` 
/add_word?word=\<word>

response type : {
    status: status code,
    msg: msg
}

```

```
* /autocomplete?query=\<query>
  
response type [
    <word 1>,
    <word 2>,
    etc
]


```

