(* tokens: integers, + - * /, semicolon , (, ) ......*)

%token <int> INT
%token PLUS
%token MINUS
%token TIMES
%token DIV
%token LPAREN
%token RPAREN
%token SEMICOLON
%token EOF
%token EQUAL
%token NOTEQUAL

%left EQUAL NOTEQUAL (* lowest precedence, left-associative *)
%left PLUS MINUS   (* second-lowest precedence , left-associative*)
%left TIMES DIV    (* medium precedence , left-associative*)
%nonassoc UMINUS   (* highest precedence *)

%start <bool option> prog
%%

(* productions *)
(* part 1 *)
(* the calculated results are accumalted in an OCaml bool list *)
(* non-terminal symbol porg is converted to a Ocaml type <bool list> *)

prog:
  | EOF { None }
  | s = statement { Some s } ;

(* expressions end with a semicolon, not with a newline character *)
statement:
  |one = expr; EQUAL; two = expr;  SEMICOLON { one = two };
  |one = expr; NOTEQUAL; two = expr; SEMICOLON { one!= two };

expr:
  | i = INT 	{ i }
  | LPAREN e = expr RPAREN	{ e }
  | e1 = expr PLUS e2 = expr	{ e1 + e2 }
  | e1 = expr MINUS e2 = expr	{ e1 - e2 }
  | e1 = expr TIMES e2 = expr 	{ e1 * e2 }
  | e1 = expr DIV e2 = expr	{ e1 / e2 }
  | MINUS e = expr %prec UMINUS	{ -e }
;

