# Music Library Manager

The goal of this problem is to create a Music Library Manager in a step-by-step process, incrementally adding features.

You will need to build a CLI (Command Line Interface) tool to solve this problem. The CLI will take in a directory as the input, and the commands that need to be executed must all run recursively over the given directory, i.e., the commands must be executed for all subdirectories of the given input directory.

You can set up the project in the language of your choice.

Please include documentation (in a file called `SETUP.md`) on any prerequisites we would need to have installed to run your program.

This exercise has included some music files to help you with test data. You can find them [here](Music/).

## Step 1: List Files

Take in one argument as input: a directory the user specifies. Your program must list out all music files in that directory to stdout.

### Expected Outcome

When a user runs the following command:

```shell
<program> --input <path to music folder> --list-files
```

The output should be something like this:

```text
Thriller.mp3
Shake It Off.mp3
Billie Jean.mp3
Bad Blood.mp3
Smooth Criminal.mp3
Anti-Hero.mp3
```

## Step 2: Show Metadata

The next step is to read and show the metadata of the files you listed in [Step 1](#step-1-list-files).

For example, an MP3 file contains information regarding the name of the Song (Billie Jean), name of the Artist (Michael Jackson), Album (Thriller), and other such information. See [this](https://en.wikipedia.org/wiki/ID3) for a reference.

You can use a library available for your language of choice to parse the metadata for a music file. If you cannot find an appropriate library, CLI tools like [ffmpeg](https://ffmpeg.org) can be used instead.

### Expected Outcome

When a user runs the following command:

```shell
<program> --input <path to music folder> --show-metadata
```

The output should be like this:

```text
____________________
File: Music/Thriller.mp3
Song: Thriller
Artist: Michael Jackson
Album: Thriller
____________________
File: Music/Shake It Off.mp3
Song: Shake It Off
Artist: Taylor Swift
Album: 1989
____________________
```

> [!NOTE]
> All the files must be listed in a similar manner, not just the first two. Files present in subdirectories must be included as well.

## Step 3: Grouping

Once you are able to read metadata, allow the user to categorise the files. Note that files aren't moved or relocated in this step at all--instead the user just views their music based on their category of choice.

Allow the user to view their library categorized by the following parameters:

- Artist
- Album
- Artist + Album

### Expected Outcome

Suppose that, in a particular music library, the user has the following songs in the `Music` folder:

```text
Music
├── Anti-Hero.mp3
├── Bad Blood.mp3
├── Billie Jean.mp3
├── Shake It Off.mp3
├── Smooth Criminal.mp3
└── Thriller.mp3
```

The user should be able to view it in the following way:

#### By Artist

When a user runs the following command:

```shell
<program> --input <path to music folder> --group-by ARTIST
```

The output is a string, printed on stdout like this:

```text
Music
├── Michael Jackson
│   ├── Billie Jean.mp3
│   ├── Smooth Criminal.mp3
│   └── Thriller.mp3
└── Taylor Swift
    ├── Anti-Hero.mp3
    ├── Bad Blood.mp3
    └── Shake It Off.mp3
```

#### By Album

When a user runs the following command:

```shell
<program> --input <path to music folder> --group-by ALBUM
```

The output is a string, printed on stdout like this:

```text
Music
├── 1989
│   ├── Bad Blood.mp3
│   └── Shake It Off.mp3
├── Bad
│   └── Smooth Criminal.mp3
├── Midnights
│   └── Anti-Hero.mp3
└── Thriller
    ├── Billie Jean.mp3
    └── Thriller.mp3
```

#### By Artist and Album

When a user runs the following command:

```shell
<program> --input <path to music folder> --group-by ARTIST_ALBUM
```

The output is a string, printed on stdout like this:

```text
Music
├── Michael Jackson
│   ├── Bad
│   │   └── Smooth Criminal.mp3
│   └── Thriller
│       ├── Billie Jean.mp3
│       └── Thriller.mp3
└── Taylor Swift
    ├── 1989
    │   ├── Bad Blood.mp3
    │   └── Shake It Off.mp3
    └── Midnights
        └── Anti-Hero.mp3
```

> [!NOTE]
> In this step, we are not changing the location of files. The scope of this step is to just display the library in a grouped manner in stdout. Moving the files to new directories will be a part of [Step 5](#step-5-reorganize-files).

## Step 4: Reorganize Files - Dry Run

The intention here is to enable users to see changes that would occur if they choose to reorganize their files in the file system based on metadata. This command should specify what changes would be made on the file system based on the criteria to reorganize by.

Note that no actual file movement should happen as part of this step - only the list of changes that would be made as part of the reorganization should be printed to stdout.

### Expected Output

#### By Artist

When a user runs the following command:

```shell
<program> --input <path to music folder> --reorganize-by ARTIST --dry-run
```

The output should be like this:

```shell
The following changes will be made to your library:

Music/Thriller.mp3 --->  Music/Michael Jackson/Thriller.mp3
Music/Shake It Off.mp3 --->  Music/Taylor Swift/Shake It Off.mp3
Music/Billie Jean.mp3 --->  Music/Michael Jackson/Billie Jean.mp3
Music/Smooth Criminal.mp3 --->  Music/Michael Jackson/Smooth Criminal.mp3
Music/Bad Blood.mp3 --->  Music/Taylor Swift/Bad Blood.mp3
Music/Anti-Hero.mp3 --->  Music/Taylor Swift/Anti-Hero.mp3
```

#### By Album

This is the similar to [By Artist](#by-artist-1), but for albums.

#### By Artist & Album

This is the similar to [By Artist](#by-artist-1), but for both artist and album. See the output of [Step 3](#step-3-grouping) for an example.

## Step 5: Reorganize Files

This is an extension to the previous step. In this step, the files should be reorganized on the file system by moving them as necessary.

### Expected Output

#### By Artist

When a user runs the following command:

```shell
<program> --input <path to music folder> --reorganize-by ARTIST
```

The output should be like this:

```shell
Moved Music/Thriller.mp3 --->  Music/Michael Jackson/Thriller.mp3
Moved Music/Shake It Off.mp3 --->  Music/Taylor Swift/Shake It Off.mp3
Moved Music/Billie Jean.mp3 --->  Music/Michael Jackson/Billie Jean.mp3
Moved Music/Smooth Criminal.mp3 --->  Music/Michael Jackson/Smooth Criminal.mp3
Moved Music/Bad Blood.mp3 --->  Music/Taylor Swift/Bad Blood.mp3
Moved Music/Anti-Hero.mp3 --->  Music/Taylor Swift/Anti-Hero.mp3
```

Note that the file should actually move as a part of this command.

#### By Album

This is the similar to [By Artist](#by-artist-2), but for albums.

#### By Artist & Album

This is the similar to [By Artist](#by-artist-2), but for both artist and album.

## Step 6: Displaying Metadata from the Internet

For files that do not have proper metadata tags, APIs can be used that would fetch the metadata from the internet. The program should make an API call to search for any songs present with the name similar to file’s name. This will return a list of matching songs, and display the possible metadata for that file accordingly.

Potentially useful APIs:

- [https://musicbrainz.org/](https://musicbrainz.org/)
- Music services like Spotify, Apple Music, and Shazam also provide APIs

Please be wary of the fact that these services often have rate limits. Calling the APIs too many times may prevent your ability to solve this part of the problem.

### Expected Outcome

When a user runs the following command:

```shell
<program> --input <path to music folder> --suggest-metadata-matches
```

The output should be like this:

```text
File: Music/Thriller.mp3
Top 3 matches:
1. Song: Thriller
   Album: The Thriller
   Artist: Dharan Kumar & Ishaan Dev
2. Song: Thriller
   Album: The Power of Classic Rock
   Artist: London Symphone Orchestra
3. Song: Thriller
   Album: Thriller
   Artist: Michael Jackson
---
File: Music/Smooth Criminal.mp3
Top 3 matches:
1. Song: Smooth Criminal
   Album: Bad
   Artist: Michael Jackson
2. Song: Unsmooth Criminal
   Album: Gang Units
   Artist: Joshua Klein
3. Song: Criminal
   Album: Tidal
   Artist: Fiona Apple
```

> [!NOTE]
> Metadata suggestions for all the files must be listed in a similar manner, not just the first two. Files present in subdirectories must be included as well.

## Step 7: Update Metadata from the Internet

This is an extension to [Step 6](#step-6-displaying-metadata-from-the-internet). In addition to displaying metadata from the internet, this command should allow a user to update the metadata in files.

### Expected Outcome

When a user runs the following command:

```shell
<program> --input <path to music folder> --update-metadata
```

The output should be like this:

```text
File: Music/Thriller.mp3
Top 3 matches:
1. Song: Thriller
   Album: The Thriller
   Artist: Dharan Kumar & Ishaan Dev
2. Song: Thriller
   Album: The Power of Classic Rock
   Artist: London Symphone Orchestra
3. Song: Thriller
   Album: Thriller
   Artist: Michael Jackson
Do you wish to update (Y/N)?
Y
Select correct choice (1, 2, 3):
2
Metadata updated.
---
File: Music/Smooth Criminal.mp3
Top 3 matches:
1. Song: Smooth Criminal
   Album: Bad
   Artist: Michael Jackson
2. Song: Unsmooth Criminal
   Album: Gang Units
   Artist: Joshua Klein
3. Song: Criminal
   Album: Tidal
   Artist: Fiona Apple
Do you wish to update (Y/N)?
N
```

> [!NOTE]
> Metadata suggestions for all the files must be listed in a similar manner, not just the first two. Files present in subdirectories must be included as well.
