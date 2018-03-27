# reddit-clone-server

* Made using Python Flask with Postgresql DB
* Deployed on Heroku(https://reddit-pregbuddy.herokuapp.com/)

# APIs

* Get list of topics - https://reddit-pregbuddy.herokuapp.com/topics/ #GET
* Add a topic - https://reddit-pregbuddy.herokuapp.com/add-topic/ #POST
	* param key required - `content` 
* Delete a topic - https://reddit-pregbuddy.herokuapp.com/delete-topic/ #POST
	* param key required - `id`
* Up Vote a topic - https://reddit-pregbuddy.herokuapp.com/up-vote/?id= #POST
* Down Vote a topic - https://reddit-pregbuddy.herokuapp.com/down-vote/?id= #POST
	* query param `id`