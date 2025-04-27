import React, { useState } from 'react';
import styles from './JobCard.module.css';

const JobCard = ({ job }) => {
  const [showDetails, setShowDetails] = useState(false);

  const toggleDetails = () => {
    setShowDetails(!showDetails);
  };

  return (
    <div className={styles.card}>
      <div className={styles.companyRow}>
        <h3 className={styles.company}>{job.Company}</h3>
      </div>
      <div className={styles.topRow}>
        <h2 className={styles.position}>{job.Role}</h2>
        <div className={styles.tags}>
          {job.Skills.Programming.map((tag, index) => (
            <span key={index} className={styles.tag}>
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className={styles.bottomRow}>
        <div className={styles.meta}>
          <span>{job.Type}</span>
        </div>

        <button className={styles.btnPrimary} onClick={toggleDetails}>
          {showDetails ? 'Hide Details' : 'Show Details'}
        </button>

        {showDetails && (
          <>
            <div className={styles.meta}>
              <h4 className={styles.meta}>Responsibilities:</h4>
              <ul>
                {job.Responsibilities.map((responsibility, index) => (
                  <li key={index} className={styles.listItem}>
                    {responsibility}
                  </li>
                ))}
              </ul>
            </div>

            <div className={styles.meta}>
              <h4 className={styles.meta}>Required Qualifications:</h4>
              <ul>
                {job.Required.map((requirement, index) => (
                  <li key={index} className={styles.listItem}>
                    {requirement}
                  </li>
                ))}
              </ul>
            </div>

            <div className={styles.meta}>
              <h4 className={styles.meta}>Benefits:</h4>
              <ul>
                {job.Benefits.map((benefit, index) => (
                  <li key={index} className={styles.listItem}>
                    {benefit}
                  </li>
                ))}
              </ul>
            </div>

            <div className={styles.meta}>
              <h4 className={styles.meta}>Skills:</h4>
              <ul>
                {Object.keys(job.Skills).map((skillCategory) => (
                  <li key={skillCategory}>
                    <strong>{skillCategory}:</strong>
                    <ul>
                      {job.Skills[skillCategory].map((skill, index) => (
                        <li key={index}>{skill}</li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}

        <div className={styles.buttons}>
          <button className={styles.btnPrimary}>Check candidate list</button>
          <button className={styles.btnDanger}>Remove Job</button>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
