## Idea of course change

Write me a discord bot module. it should read a json out of this folder:
{
    "TIME-FORMAT": "dd-mm",
    "SUMMER_TERM": {
        "name": "Summer Term",
        "start_date": "01-04",
        "end_date": "30-09",
        "CATEGORY_ID": "1105534816658669669"
    },
    "WINTER_TERM": {
        "name": "Winter Term",
        "start_date": "01-10",
        "end_date": "31-03",
        "CATEGORY_ID": "1065377828402643044"
    },

    "SUMMER_IDS": [
    ],
    "WINTER_IDS": [
    ]
}

The json contains ids of text channels and categories. and a time frame when the two semesters start and end.
The bot should check the current date and time and compare it with the start and end dates of the two semesters.
The bot should move the channels from one category to another depending on the current date and time.
The bot should check every day in which time frame we are and move the channels from the [CURRENT] category to the [STORAGE] (the one that isnt the current semester term) category and vice versa.
If the time frame is not met, the bot should do nothing.

The bot should also have a command to add or remove channels from the json file. The command should be:
- !add_channel <channel_id> <category_id>
- !remove_channel <channel_id> <category_id>
- !list_channels <category_id>
- !list_categories
Also change the summer term and winter term category ids in the json file.
- !set_summer_term <start_date> <end_date> (dd-mm)
- !set_winter_term <start_date> <end_date> (dd-mm)
- !set_summer_category <category_id>
- !set_winter_category <category_id>