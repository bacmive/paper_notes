#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdarg.h>
#include <stdlib.h>

static void
die (const char * fmt, ...) //
{
  va_list ap;
  fprintf (stderr, "*** k-ind_aig: ");
  va_start (ap, fmt);
  vfprintf (stderr, fmt, ap);
  va_end (ap);
  fputc ('\n', stderr);
  exit (1);
}


int
main(int argc, char **argv){
	die ("at most one of '-a', '-r', '-m', '-d', or '-n' can be used");

	return 0;
}