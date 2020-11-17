(* lexer analysis *)
{
open Lexing
open Parser
exception Error of string

let next_line lexbuf =
  let pos = lexbuf.lex_curr_p in
  lexbuf.lex_curr_p <-
	{ pos with pos_bol = lexbuf.lex_curr_pos;
		pos_lnum = pos.pos_lnum + 1
	}
}

let int = ['0'-'9'] ['0'-'9']*   (* int regular expression *)

rule tokenize = 
  parse
  | [' ' '\t' '\n']	{ tokenize lexbuf}
  | ';'			{ SEMICOLON }
  | int			{ INT (int_of_string (Lexing.lexeme lexbuf)) }
  | '+'			{ PLUS }
  | '-'			{ MINUS }
  | '*' 		{ TIMES }
  | '/'			{ DIV }
  | '('			{ LPAREN }
  | ')' 		{ RPAREN }
  | '='     { EQUAL }
  | "!="    { NOTEQUAL }
  | eof			{ EOF }
  | _ 			{ raise (Error (Printf.sprintf " At offset %d: unexpected character.\n" (Lexing.lexeme_start lexbuf))) }
