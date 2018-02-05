# marsrover-pipeline
MarsRover.io backend pipeline for processing not done on AWS

In other words, this is the processing done on our personal servers and then pushed up to AWS on a regular basis.

## Dependencies
*	Python 3 (Yes, 3. Python 2 is going to be dead very soon...)
*	Python [Requests](http://docs.python-requests.org/en/master/)
*	Python AWS SDK, [boto 3](https://aws.amazon.com/sdk-for-python/)

## Configuration
marsrover-pipeline expects a config file in the user's home directory named `.marsroverio`.
It is a JSON file containing system-specific paths for the pipline. Example config:

	{
		"manifest_path" : {
			"mera" : "/path/to/spirit/metadata/dir/",
			"merb" : "/path/to/oppy/metadata/dir/",
			"msl" : "/path/to/msl/metadata/dir/",
			"m20" : "/path/to/m2020/metadata/dir/",
			"nsyt" : "/path/to/nsyt/metadata/dir/"
		}
	}

