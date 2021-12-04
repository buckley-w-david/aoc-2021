use std::fs::read_to_string;
use std::num::ParseIntError;
use std::str::FromStr;

#[derive(Clone, Copy, Debug)]
struct Mark((u64, bool));

#[derive(Debug, Clone)]
struct Board {
    numbers: [[Mark; 5]; 5],
}

impl FromStr for Board {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut rows = s.split("\n").map(|l| l.split_whitespace());
        let mut numbers = [[Mark((0, false)); 5]; 5];

        for i in 0..5 {
            let mut row = rows.next().unwrap();
            for j in 0..5 {
                let col = row.next().unwrap();
                numbers[i][j].0 .0 = col.parse()?;
                numbers[i][j].0 .1 = false;
            }
        }

        Ok(Board { numbers })
    }
}

impl Board {
    pub fn mark(&mut self, number: u64) {
        for row in &mut self.numbers {
            for entry in row {
                if entry.0 .0 == number {
                    entry.0 .1 = true;
                }
            }
        }
    }

    pub fn won(&self) -> bool {
        for row in &self.numbers {
            if row.iter().all(|cell| cell.0 .1) {
                return true;
            }
        }
        for col_idx in 0..5 {
            if self.numbers.iter().all(|row| row[col_idx].0 .1) {
                return true;
            }
        }
        false
    }

    pub fn score(&self, last_called: u64) -> u64 {
        let s: u64 = self.numbers
            .iter()
            .flat_map(|row| row.iter().filter(|cell| !cell.0 .1).map(|c| c.0 .0))
            .sum();
        s * last_called
    }
}

fn part_one(mut boards: Vec<Board>, numbers: &Vec<u64>) -> u64 {
    let mut drawn = 0;
    for &n in numbers {
        drawn = n;
        for board in boards.iter_mut() {
            board.mark(n);
        }

        if boards.iter().any(|b| b.won()) {
            break;
        }
    }

    let won = boards.iter().find(|b| b.won()).unwrap();
    won.score(drawn)
}

fn part_two(mut boards: Vec<Board>, numbers: &Vec<u64>) -> u64 {
    let mut drawn = 0;
    for &n in numbers {
        drawn = n;
        for board in boards.iter_mut() {
            board.mark(n);
        }

        if boards.len() == 1 {
            if boards.iter().any(|b| b.won()) {
                break;
            }
        }
        // Discard boards that have already won
        boards.retain(|b| !b.won()); 
    }

    let last = boards.iter().find(|b| b.won()).unwrap();
    last.score(drawn)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let input = read_to_string("input")?;
    let mut sections = input.split("\n\n");
    let numbers = sections
        .next()
        .unwrap()
        .split(",")
        .map(|n| n.parse().unwrap())
        .collect();
    let boards: Vec<Board> = sections.map(|b| b.trim().parse().unwrap()).collect();

    let p1_boards = boards.clone();
    let p2_boards = boards.clone();

    println!("Part 1: {}", part_one(p1_boards, &numbers));
    println!("Part 2: {}", part_two(p2_boards, &numbers));

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn example_data() -> (Vec<u64>, Vec<Board>) {
        let ns = vec![
            7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19,
            3, 26, 1,
        ];
        let boards = vec![
            Board {
                numbers: [
                    [
                        Mark((3, false)),
                        Mark((15, false)),
                        Mark((0, false)),
                        Mark((2, false)),
                        Mark((22, false)),
                    ],
                    [
                        Mark((9, false)),
                        Mark((18, false)),
                        Mark((13, false)),
                        Mark((17, false)),
                        Mark((5, false)),
                    ],
                    [
                        Mark((19, false)),
                        Mark((8, false)),
                        Mark((7, false)),
                        Mark((25, false)),
                        Mark((23, false)),
                    ],
                    [
                        Mark((20, false)),
                        Mark((11, false)),
                        Mark((10, false)),
                        Mark((24, false)),
                        Mark((4, false)),
                    ],
                    [
                        Mark((14, false)),
                        Mark((21, false)),
                        Mark((16, false)),
                        Mark((12, false)),
                        Mark((6, false)),
                    ],
                ],
            },
            Board {
                numbers: [
                    [
                        Mark((14, false)),
                        Mark((21, false)),
                        Mark((17, false)),
                        Mark((24, false)),
                        Mark((4, false)),
                    ],
                    [
                        Mark((10, false)),
                        Mark((16, false)),
                        Mark((15, false)),
                        Mark((9, false)),
                        Mark((19, false)),
                    ],
                    [
                        Mark((18, false)),
                        Mark((8, false)),
                        Mark((23, false)),
                        Mark((26, false)),
                        Mark((20, false)),
                    ],
                    [
                        Mark((22, false)),
                        Mark((11, false)),
                        Mark((13, false)),
                        Mark((6, false)),
                        Mark((5, false)),
                    ],
                    [
                        Mark((2, false)),
                        Mark((0, false)),
                        Mark((12, false)),
                        Mark((3, false)),
                        Mark((7, false)),
                    ],
                ],
            },
        ];
        (ns, boards)
    }

    #[test]
    fn test_part_one() {
        let (ns, boards) = example_data();
        let res = part_one(boards, &ns);
        assert_eq!(res, 4512);
    }

    #[test]
    fn test_part_two() {
        let (ns, boards) = example_data();
        let res = part_two(boards, &ns);
        assert_eq!(res, 1924);
    }
}
