use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

use std::num::ParseIntError;
use std::str::FromStr;

enum Command {
    Forward,
    Up,
    Down,
}

struct Instruction {
    command: Command,
    measure: u64,
}

impl FromStr for Instruction {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts: Vec<&str> = s.trim().split(' ').collect();

        let measure = parts.pop().unwrap().parse()?;

        let command = match parts.pop().unwrap() {
            "forward" => Command::Forward,
            "up" => Command::Up,
            "down" => Command::Down,
            _ => unreachable!(),
        };

        Ok(Instruction { command, measure })
    }
}

fn part_one(instructions: &Vec<Instruction>) -> Result<u64, Box<dyn std::error::Error>> {
    let mut depth = 0;
    let mut horizontal = 0;
    for instr in instructions {
        match instr.command {
            Command::Forward => horizontal += instr.measure,
            Command::Up => depth -= instr.measure,
            Command::Down => depth += instr.measure,
        }
    }
    Ok(depth * horizontal)
}

fn part_two(instructions: &Vec<Instruction>) -> Result<u64, Box<dyn std::error::Error>> {
    let mut depth = 0;
    let mut horizontal = 0;
    let mut aim = 0;
    for instr in instructions {
        match instr.command {
            Command::Forward => {
                horizontal += instr.measure;
                depth += aim * instr.measure;
            }
            Command::Up => aim -= instr.measure,
            Command::Down => aim += instr.measure,
        }
    }
    Ok(depth * horizontal)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input")?;
    let instructions = BufReader::new(file)
        .lines()
        .map(|l| l.unwrap().parse().unwrap())
        .collect();
    println!("Part 1: {}", part_one(&instructions)?);
    println!("Part 2: {}", part_two(&instructions)?);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn example_data() -> Vec<Instruction> {
        vec![
            Instruction {
                command: Command::Forward,
                measure: 5,
            },
            Instruction {
                command: Command::Down,
                measure: 5,
            },
            Instruction {
                command: Command::Forward,
                measure: 8,
            },
            Instruction {
                command: Command::Up,
                measure: 3,
            },
            Instruction {
                command: Command::Down,
                measure: 8,
            },
            Instruction {
                command: Command::Forward,
                measure: 2,
            },
        ]
    }

    #[test]
    fn test_part_one() {
        let input = example_data();
        let res = part_one(&input);
        assert_eq!(res.unwrap(), 150);
    }

    #[test]
    fn test_part_two() {
        let input = example_data();
        let res = part_two(&input);
        assert_eq!(res.unwrap(), 900);
    }
}
