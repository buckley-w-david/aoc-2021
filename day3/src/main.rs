use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

fn part_one(diagnostics: &Vec<u64>, length: u64) -> u64 {
    let mut ones = vec![0; length as usize];
    let mut zeros = vec![0; length as usize];
    for measure in diagnostics {
        for i in 0..length {
            let peek = (measure & (1 << i)) >> i;
            if peek == 1 {
                ones[i as usize] += 1;
            } else {
                zeros[i as usize] += 1;
            }
        }
    }
    let mut gamma = 0;
    let mut epsilon = 0;
    for i in 0..length {
        let o = ones[i as usize];
        let z = zeros[i as usize];
        if o > z {
            gamma = gamma | (1 << i);
        }

        if z > o {
            epsilon = epsilon | (1 << i);
        }
    }

    gamma * epsilon
}

fn part_two(diagnostics: &Vec<u64>, length: u64) -> u64 {
    let mut ogr_candidates = diagnostics.clone();
    let mut co2_candidates = diagnostics.clone();

    let mut idx = length;
    while ogr_candidates.len() != 1 {
        idx -= 1;

        let mut ones = 0;
        let mut zeros = 0;
        for measure in &ogr_candidates {
            let peek = (measure & (1 << idx)) >> idx;
            if peek == 1 {
                ones += 1;
            } else {
                zeros += 1;
            }
        }

        let most_common = if ones >= zeros {
            1
        } else {
            0
        };

        ogr_candidates.retain(|ogr| ((ogr & (1 << idx)) >> idx) == most_common);
    }

    let mut idx = length;
    while co2_candidates.len() != 1 {
        idx -= 1;

        let mut ones = 0;
        let mut zeros = 0;
        for measure in &co2_candidates {
            let peek = (measure & (1 << idx)) >> idx;
            if peek == 1 {
                ones += 1;
            } else {
                zeros += 1;
            }
        }

        let least_common = if ones >= zeros {
            0
        } else {
            1
        };

        co2_candidates.retain(|co2| (co2 & (1 << idx)) >> idx == least_common);
    }

    ogr_candidates.pop().unwrap() * co2_candidates.pop().unwrap()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input")?;
    let diagnostics: Vec<u64> = BufReader::new(file)
        .lines()
        .map(|l| u64::from_str_radix(&l.unwrap(), 2).unwrap())
        .collect();
    println!("Part 1: {}", part_one(&diagnostics, 12));
    println!("Part 2: {}", part_two(&diagnostics, 12));

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn example_data() -> Vec<u64> {
        vec![
            0b00100,
            0b11110,
            0b10110,
            0b10111,
            0b10101,
            0b01111,
            0b00111,
            0b11100,
            0b10000,
            0b11001,
            0b00010,
            0b01010,
        ]
    }

    #[test]
    fn test_part_one() {
        let input = example_data();
        let res = part_one(&input, 5);
        assert_eq!(res, 198);
    }

    #[test]
    fn test_part_two() {
        let input = example_data();
        let res = part_two(&input, 5);
        assert_eq!(res, 230);
    }
}
