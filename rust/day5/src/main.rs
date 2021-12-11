use std::fmt;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::str::FromStr;
use std::collections::HashMap;

type Result<T> = std::result::Result<T, LineSegmentError>;

#[derive(Debug, Clone)]
struct LineSegmentError;

impl fmt::Display for LineSegmentError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid line segment")
    }
}

#[derive(Debug)]
struct LineSegment {
    pub x1: i64,
    pub y1: i64,
    pub x2: i64,
    pub y2: i64,
}

impl LineSegment {
    // This relies on the fact that we only have to deal with vertical, horizontal, or 45 degree
    // lines to operate correctly.
    pub fn points(&self) -> Vec<(i64, i64)> {
        let dx = self.x2 - self.x1;
        let dy = self.y2 - self.y1;

        let x_dir = dx.signum();
        let y_dir = dy.signum();

        let mut points = Vec::new();
        for i in 0..i64::max(dx.abs(), dy.abs())+1 {
            points.push((self.x1+i*x_dir, self.y1+i*y_dir));
        }
        points
    }
}

impl FromStr for LineSegment {
    type Err = LineSegmentError;

    fn from_str(s: &str) -> Result<Self> {
        let mut coords = s.split(" -> ");
        let mut x1y1 = coords.next().ok_or(LineSegmentError)?.split(",");
        let x1 = x1y1.next().ok_or(LineSegmentError)?.parse().map_err(|_| LineSegmentError)?;
        let y1 = x1y1.next().ok_or(LineSegmentError)?.parse().map_err(|_| LineSegmentError)?;
        let mut x2y2 = coords.next().ok_or(LineSegmentError)?.split(",");
        let x2 = x2y2.next().ok_or(LineSegmentError)?.parse().map_err(|_| LineSegmentError)?;
        let y2 = x2y2.next().ok_or(LineSegmentError)?.parse().map_err(|_| LineSegmentError)?;

        Ok(LineSegment { x1, y1, x2, y2 })
    }
}

fn part_one(coordinates: &Vec<LineSegment>) -> i64 {
    let mut counts = HashMap::new();
    for segment in coordinates {
        // Part 1 specific
        if segment.x1 != segment.x2 && segment.y1 != segment.y2 {
            continue;
        }
        let points = segment.points();
        for point in points {
            let count = counts.entry(point).or_insert(0);
            *count += 1;
        }
    }
    let mut s = 0;
    for (_, value) in counts {
        if value > 1 {
            s += 1;
        }
    }
    s
}

fn part_two(coordinates: &Vec<LineSegment>) -> i64 {
    let mut counts = HashMap::new();
    for segment in coordinates {
        let points = segment.points();
        for point in points {
            let count = counts.entry(point).or_insert(0);
            *count += 1;
        }
    }
    let mut s = 0;
    for (_, value) in counts {
        if value > 1 {
            s += 1;
        }
    }
    s

}

fn main() -> Result<()> {
    let file = File::open("input").map_err(|_| LineSegmentError)?;
    let coordinates = BufReader::new(file)
        .lines()
        .map(|l| l.unwrap().parse().unwrap())
        .collect();
    println!("Part 1: {}", part_one(&coordinates));
    println!("Part 2: {}", part_two(&coordinates));

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn example_data() -> Vec<LineSegment> {
        vec![
            LineSegment {x1: 0, y1: 9, x2: 5, y2: 9},
            LineSegment {x1: 8, y1: 0, x2: 0, y2: 8},
            LineSegment {x1: 9, y1: 4, x2: 3, y2: 4},
            LineSegment {x1: 2, y1: 2, x2: 2, y2: 1},
            LineSegment {x1: 7, y1: 0, x2: 7, y2: 4},
            LineSegment {x1: 6, y1: 4, x2: 2, y2: 0},
            LineSegment {x1: 0, y1: 9, x2: 2, y2: 9},
            LineSegment {x1: 3, y1: 4, x2: 1, y2: 4},
            LineSegment {x1: 0, y1: 0, x2: 8, y2: 8},
            LineSegment {x1: 5, y1: 5, x2: 8, y2: 2},
        ]
    }

    #[test]
    fn test_part_one() {
        let input = example_data();
        let res = part_one(&input);
        assert_eq!(res, 5);
    }

    #[test]
    fn test_part_two() {
        let input = example_data();
        let res = part_two(&input);
        assert_eq!(res, 12);
    }
}
