#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stats.h"
#include "trace.h"

int collect_key_value_file(struct stats *stats, const char *path)
{
  int rc = 0;
  FILE *file = NULL;
  char *line = NULL;
  size_t line_size = 0;

  file = fopen(path, "r");
  if (file == NULL) {
    ERROR("cannot open `%s': %m\n", path);
    rc = -1;
    goto out;
  }

  while (getline(&line, &line_size, file) >= 0) {
    char *key, *rest = line;
    unsigned long long val;

    key = strsep(&rest, " \t\n");
    if (key[0] == 0)
      continue;
    if (rest == NULL)
      continue;

    errno = 0;
    val = strtoull(rest, NULL, 0);
    if (errno == 0)
      stats_set(stats, key, val);
  }

 out:
  free(line);
  if (file != NULL)
    fclose(file);

  return rc;
}