import os
import sys


LICENSE_HEADER = """/*
   Copyright 2018 Alexandru-Paul Copil

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/


"""

IGNORE_LIST = [".git", "build", "dist"]
EXTENSION = ".s"

for path, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith(EXTENSION):
            full_path = os.path.join(path, file)
            has_copyright = False

            lines = []
            with open(full_path, "r") as fp:
                lines = fp.readlines()
                for line in lines:
                    if "Copyright 2018 Alexandru-Paul Copil" in line:
                        has_copyright = True

            if not has_copyright:
                print("modified: ", full_path)
                lines.insert(0, LICENSE_HEADER)
                with open(full_path, "w") as fp:
                    fp.writelines(lines)
