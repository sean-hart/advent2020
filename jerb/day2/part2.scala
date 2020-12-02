// aoc 2020 day2 part 2
import scala.io.Source

val inputFile = "input.txt"

case class PasswordTest(
  pos1: Int,
  pos2: Int,
  char: Char,
  password: String
)


def parseLine(line: String): PasswordTest = {
  val re = """(\d+)-(\d+) ([a-zA-Z]): ([a-zA-Z]+)""".r
  line match {
    case re(p1, p2, c, pw) => PasswordTest(p1.toInt, p2.toInt, c(0), pw)
    case _ => throw new IllegalArgumentException("invalid line: " + line)
  }
}


def isValidPassword(test: PasswordTest) = 
  (test.char == test.password.charAt(test.pos1 - 1)) ^
  (test.char == test.password.charAt(test.pos2 - 1))

def solution(inputFile: String): Int =
  Source.fromFile(inputFile)
    .getLines()
    .map(parseLine)
    .filter(isValidPassword(_))
    .length

println(solution(inputFile))

