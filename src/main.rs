use std::collections::HashSet;
use chrono::{prelude::*, Months, Duration};

#[derive(Debug)]
struct DateBucket {
  capacity: usize,
  datefmt: &'static str,
  hashset: HashSet<String>,
}

impl DateBucket {

  // create an empty bucket
  fn new (datefmt: &'static str, capacity: usize) -> DateBucket {
    return DateBucket { capacity, datefmt, hashset: vec![].into_iter().collect() };
  }
  
  // try to insert a new date into the bucket
  fn add (&mut self, dt: DateTime<Utc>) -> bool {
    // bucket is already full
    if self.hashset.len() >= self.capacity {
      return false;
    }
    // else try to insert ..
    return self.hashset.insert(dt.format(self.datefmt).to_string());
  }

}

#[derive(Debug)]
struct DateSieve {
  buckets: [DateBucket; 7],
}

impl DateSieve {

  // create a fresh sieve
  fn new (seconds: usize, minutes: usize, hours: usize, days: usize, weeks: usize, months: usize, years: usize) -> DateSieve {
    return DateSieve { buckets: [
      DateBucket::new("%Y-%m-%d %H:%M:%S", seconds),
      DateBucket::new("%Y-%m-%d %H:%M", minutes),
      DateBucket::new("%Y-%m-%d %H", hours),
      DateBucket::new("%Y-%m-%d", days),
      DateBucket::new("%Y %W", weeks),
      DateBucket::new("%Y-%m", months),
      DateBucket::new("%Y", years),
    ] };
  }

  // try to insert a new date into any bucket
  fn add (&mut self, dt: DateTime<Utc>) -> bool {
    let mut added = false;
    for bucket in &mut self.buckets {
      if bucket.add(dt) { added = true; }
    }
    // let added = self.buckets.map(|mut b| b.add(dt));
    // return added.contains(&true);
    return added;
  }

}



fn main() {
  
  // let mut months: DateBucket = DateBucket::new("%Y-%m", 5);
  let mut sieve: DateSieve = DateSieve::new(2, 5, 2, 3, 2, 4, 2);
  
  // chrono stuff
  let utc = Utc::now();
  println!("now: {:?}", utc);
  println!("sieve [init]: {:?}\n", sieve);

  // try filling all buckets
  for sec in 1.. {
    if sieve.add(utc + Duration::seconds(sec)) { println!("sieve [+{:02}s]: {:?}\n", sec, sieve); }
    else { break };
  };
  for min in 1.. {
    if sieve.add(utc + Duration::minutes(min)) { println!("sieve [+{:02}m]: {:?}\n", min, sieve); }
    else { break };
  };
  for hrs in 1.. {
    if sieve.add(utc + Duration::hours(hrs)) { println!("sieve [+{:02}h]: {:?}\n", hrs, sieve); }
    else { break };
  };
  for dys in 1.. {
    if sieve.add(utc + Duration::days(dys)) { println!("sieve [+{:02}d]: {:?}\n", dys, sieve); }
    else { break };
  };
  for wks in 1.. {
    if sieve.add(utc + Duration::weeks(wks)) { println!("sieve [+{:02}w]: {:?}\n", wks, sieve); }
    else { break };
  };
  for mon in 1.. {
    if sieve.add(utc + Months::new(mon)) { println!("sieve [+{:02}M]: {:?}\n", mon, sieve); }
    else { break };
  };
  for yrs in 1.. {
    if sieve.add(utc + Months::new(yrs*12)) { println!("sieve [+{:02}y]: {:?}\n", yrs, sieve); }
    else { break };
  };


  let mut i: u8 = 1;
  while sieve.add(utc + Months::new(i.into())) {
    i += 1;
  }

}
