# marsrover-pipeline
MarsRover.io backend pipeline for processing not done on AWS

In other words, this is the processing done on our personal servers and then pushed up to AWS on a regular basis.

## License

See the LICENSE file for full license text.

Copyright 2018 nmrossomando and camdenmil

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this code except in compliance with the License.
You may obtain a copy of the License [here](http://www.apache.org/licenses/LICENSE-2.0)
or in the LICENSE file of this repository.

Unless required by applicable law or agreed to in writing, software
distributed under the Liccense is distributed in an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, eith express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Dependencies
*	Python 3 (Yes, 3. Python 2 is going to be dead very soon...)
*	Python [Requests](http://docs.python-requests.org/en/master/)
*	Python AWS SDK, [boto 3](https://aws.amazon.com/sdk-for-python/)
*	Python OpenCV bindings, python-opencv (`sudo pip3 install opencv-python`)
	*	The above will also install numpy, if it isn't already installed.

## Configuration
marsrover-pipeline expects a config file in the user's home directory named `.marsroverio`.
It is a JSON file containing system-specific paths for the pipeline. Example config:

	{
		"manifest_path" : "/path/to/metadata/dir/",
		"images_path" : "/path/to/images/dir/"
	}

## Testing
Each file in the repository is self-testing. Because of Python's limitiations on imports when running a file
directly, however, you must run each, as a module, from the root directory. example:

    marsrover-pipeline $ python3 -m metadata.manifest

