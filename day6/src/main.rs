use std::fs::read_to_string;

fn population_size(inital: &Vec<u8>, generations: u64) -> u64 {
    let mut state = [0; 9];
    for fish in inital {
        state[*fish as usize] += 1;
    }

    for _ in 0..generations {
        state.rotate_left(1);
        state[6] += state[8];
    }

    state.iter().sum()
}

fn part_one(population: &Vec<u8>) -> u64 {
    population_size(population, 80)
}

fn part_two(population: &Vec<u8>) -> u64 {
    population_size(population, 256)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let population = read_to_string("input")?.trim().split(",").map(|i| i.parse().unwrap()).collect();
    println!("Part 1: {}", part_one(&population));
    println!("Part 2: {}", part_two(&population));

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn example_data() -> Vec<u8> {
        vec![3,4,3,1,2]
    }

    #[test]
    fn test_part_one() {
        let population = example_data();
        let res = part_one(&population);
        assert_eq!(res, 5934);
    }

    #[test]
    fn test_part_two() {
        let population = example_data();
        let res = part_two(&population);
        assert_eq!(res, 26984457539);
    }
}
