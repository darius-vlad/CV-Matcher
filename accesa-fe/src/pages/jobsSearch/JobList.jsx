import React, { useEffect, useState } from 'react';
import JobCard from '../../components/jobCard/JobCard';
import SearchBar from '../../components/searchBar/Searchbar';
import styles from './JobList.module.css';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/get-all-jobs');
        const data = await response.json();
        console.log(data)
        setJobs(data);
        setFilteredJobs(data);
      } catch (err) {
        console.error('Error fetching jobs:', err);
      }
    };

    fetchJobs();
  }, []);

  const handleSearch = (term) => {
    setSearchTerm(term);

    const filtered = jobs.filter(
      (job) =>
        job.Role.toLowerCase().includes(term.toLowerCase()) ||
        job.Company.toLowerCase().includes(term.toLowerCase())
    );

    setFilteredJobs(filtered);
  };

  return (
    <div className={styles.jobListContainer}>
      <SearchBar value={searchTerm} onChange={handleSearch} />

      <div className={styles.jobList}>
        {filteredJobs.length > 0 ? (
          filteredJobs.map((job, index) => <JobCard key={index} job={job} />)
        ) : (
          <p>No jobs match your search.</p>
        )}
      </div>
    </div>
  );
};

export default JobList;