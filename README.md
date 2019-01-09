# datesieve

`datesieve.py` is a script to filter through a list of filenames or other entries with dates and
only keep specific entries according to retention policies. It is inspired by the way
[restic](https://restic.net/) handles its
[snapshot policies](https://github.com/restic/restic/blob/master/internal/restic/snapshot_policy.go).

## synopsis

You give it a list of date objects and specify how many hourly, daily, weekly, ... entries you want
to keep. It then uses `strftime()` and sets to see if the desired amount was reached and sieves out
anything else. Here is table illustrating which entries would be kept if you want to keep 3 daily, 5
weekly and 4 monthly entries:

| original date | 3 daily / `%Y%m%d` | 5 weekly / `%Y%W` | 4 monthly / `%Y%m` | keep? |
| :-----------: | :----------------: | :---------------: | :----------------: | :---: |
|  2019-01-09   |    **20190109**    |    **201902**     |     **201901**     |   ✓   |
|  2019-01-04   |    **20190104**    |    **201901**     |       201901       |   ✓   |
|  2018-12-30   |    **20181230**    |    **201852**     |     **201812**     |   ✓   |
|  2018-12-25   |      20181225      |      201852       |       201812       |       |
|  2018-12-20   |      20181220      |    **201851**     |       201812       |   ✓   |
|  2018-12-15   |      20181215      |    **201850**     |       201812       |   ✓   |
|  2018-12-10   |      20181210      |      201850       |       201812       |       |
|  2018-12-05   |      20181205      |      201849       |       201812       |       |
|  2018-11-30   |      20181130      |      201848       |     **201811**     |   ✓   |
|  2018-11-25   |      20181125      |      201847       |       201811       |       |
|  2018-11-20   |      20181120      |      201847       |       201811       |       |

## usage

Sticking to the mantra of keeping things simple and handling text streams well, it is mainly
intended for usage in shell scripts and brings some substitution functionality with regular
expressions, so you can easily handle lists of complicated filenames. The following example shows
how to handle a file listing of a directory with daily Gitlab backup archives:

```
[...]
/zfs/backup/gitlab/1542668437_2018_11_20_11.4.5_gitlab_backup.tar
/zfs/backup/gitlab/1542754838_2018_11_21_11.4.5_gitlab_backup.tar
/zfs/backup/gitlab/1542841237_2018_11_22_11.4.5_gitlab_backup.tar
[...]
/zfs/backup/gitlab/1543964437_2018_12_05_11.4.5_gitlab_backup.tar
/zfs/backup/gitlab/1544001325_2018_12_05_11.4.5_gitlab_backup.tar
/zfs/backup/gitlab/1544050835_2018_12_06_11.5.2_gitlab_backup.tar
/zfs/backup/gitlab/1544137236_2018_12_07_11.5.2_gitlab_backup.tar
[...]
/zfs/backup/gitlab/1546729240_2019_01_06_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546815640_2019_01_07_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546902039_2019_01_08_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546988439_2019_01_09_11.6.1_gitlab_backup.tar
```

To parse the date from the UNIX epoch in the filename and keep **7 daily** and **52 weekly** backups
you could use the following command:

```sh
$ ls /zfs/backup/gitlab/*backup.tar |\
  ./datesieve.py --resub '.*/([0-9]+)_.*' '\1' --strptime '%s' \
  --inclusive --sort --days 7 --weeks 52

/zfs/backup/gitlab/1546988439_2019_01_09_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546902039_2019_01_08_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546815640_2019_01_07_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546729240_2019_01_06_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546642839_2019_01_05_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546556439_2019_01_04_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546470040_2019_01_03_11.6.1_gitlab_backup.tar
/zfs/backup/gitlab/1546210840_2018_12_31_11.5.2_gitlab_backup.tar
/zfs/backup/gitlab/1546124439_2018_12_30_11.5.2_gitlab_backup.tar
/zfs/backup/gitlab/1545519640_2018_12_23_11.5.2_gitlab_backup.tar
/zfs/backup/gitlab/1544914839_2018_12_16_11.5.2_gitlab_backup.tar
/zfs/backup/gitlab/1544310036_2018_12_09_11.5.2_gitlab_backup.tar
/zfs/backup/gitlab/1543705237_2018_12_02_11.4.5_gitlab_backup.tar
/zfs/backup/gitlab/1543100436_2018_11_25_11.4.5_gitlab_backup.tar
[...]
```

Note that `%s` is not normally a valid format for `strptime` - the script handles the special case
of `--strptime %s` by using `datetime.fromtimestamp()` instead. The two arguments for `--resub` are
the pattern and replacement respectively, i.e. as in `re.sub($pattern, $replacement, $string)`, and
the result of this substitution will be parsed as a date. If no `strptime` format is given,
`dateutil.parse(..., fuzzy=True)` is used, which should cover most sane cases correctly.

Omitting `--inclusive` would output filenames _to be deleted_ and omitting `--sort` would assume
that the entries are sorted newest-first already and just start line-by-line directly.

## license

This work is license under the [MIT License](LICENSE).