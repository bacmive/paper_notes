open Core.Std
open Lexer
open Lexing

(* print the current position *)
let print_position outx lexbuf =
  let pos = lexbuf.lex_curr_p in
  fprintf outx "%s:%d:%d" pos.pos_fname
    pos.pos_lnum (pos.pos_cnum - pos.pos_bol + 1)

let parse_with_error lexbuf = 
  try Parser.prog Lexer.tokenize lexbuf with
  | Error msg -> 
    fprintf stderr "%a: %s\n" print_position lexbuf msg;
    []
  | Parser.Error ->
    fprintf stderr "\n%a: syntax error\n" print_position lexbuf;
    exit(-1)

let print_bool_list lexbuf = 
  match parse_with_error lexbuf with
  | stmt :: p as l -> 
    List.iter ~f:(fun i -> printf "%b; " i) l ;
    printf "\n"
  | stmt -> ()


let loop filename () =
  let inx = In_channel.create filename in
  let filebuf = Lexing.from_channel inx in
  filebuf.lex_curr_p <- { filebuf.lex_curr_p with pos_fname = filename };
  print_bool_list filebuf;
  In_channel.close inx

let () =
  Command.basic ~summary:"Print boolean list"
    Command.Spec.(empty +> anon ("filename" %: string))
    loop
  |> Command.run


