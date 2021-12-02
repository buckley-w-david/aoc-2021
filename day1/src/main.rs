use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

fn part_one(depths: &Vec<u64>) -> Result<u64, Box<dyn std::error::Error>> {
    let mut depth = depths.first().unwrap();
    let mut increases = 0;
    for d in depths[1..].iter() {
        if d > depth {
            increases += 1;
        }
        depth = d;
    }
    Ok(increases)
}

fn part_two(depths: &Vec<u64>) -> Result<u64, Box<dyn std::error::Error>> {
    let mut windows = depths.iter().zip(depths[1..].iter()).zip(depths[2..].iter());
    let ((a, b), c) = windows.next().unwrap();
    let mut sum = a+b+c;
    let mut increases = 0;
    for ((a, b), c) in windows {
        let s = a+b+c;
        if s > sum {
            increases += 1;
        }
        sum = s;
    }
    Ok(increases)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input")?;
    let depths: Vec<u64> = BufReader::new(file)
        .lines()
        .map(|l| l.unwrap().parse().unwrap())
        .collect();
    println!("Part 1: {}", part_one(&depths)?);
    println!("Part 2: {}", part_two(&depths)?);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn example_data() -> Vec<u64> {
        vec![
            199,
            200,
            208,
            210,
            200,
            207,
            240,
            269,
            260,
            263,
        ]
    }

    #[test]
    fn test_part_one() {
        let input = example_data();
        let res = part_one(&input);
        assert_eq!(res.unwrap(), 7);
    }

    #[test]
    fn test_part_two() {
        let input = example_data();
        let res = part_two(&input);
        assert_eq!(res.unwrap(), 5);
    }
}
