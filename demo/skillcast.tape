Output demo/skillcast-demo.gif
Set Theme "Dracula"
Set Width 800
Set Height 600
Set FontSize 14
Set Padding 4
Set Framerate 24
Set PlaybackSpeed 1

Hide
Type "pip install skillcast"
Enter
Sleep 2s

Show
Type "skillcast list"
Enter
Sleep 1s

Type ""
Enter
Sleep 500ms

Type "# Create a Skill template"
Enter
Sleep 300ms
Type "skillcast init java-interview"
Enter
Sleep 1s

Type ""
Enter
Sleep 500ms

Type "# Show the generated YAML"
Enter
Sleep 300ms
Type "cat java-interview.yaml"
Enter
Sleep 1.5s

Type ""
Enter
Sleep 500ms

Type "# Convert to all platforms"
Enter
Sleep 300ms
Type "skillcast convert java-interview.yaml --all -o output"
Enter
Sleep 1s

Type ""
Enter
Sleep 500ms

Type "# See what we got"
Enter
Sleep 300ms
Type "ls -1 output/"
Enter
Sleep 500ms

Type ""
Enter
Sleep 300ms
Type "bat output/java-interview.claude.md || cat output/java-interview.claude.md"
Enter
Sleep 2s

Type "# Done! pip install skillcast"
Enter
Sleep 1s

Hide
Ctrl+D
