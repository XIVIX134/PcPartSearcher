import { useState } from 'react';
import '../styles/Account.css';

interface UserProfile {
  name: string;
  email: string;
  location: string;
}

export const AccountPage = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const [profile, setProfile] = useState<UserProfile>({
    name: 'User Name', // Placeholder
    email: 'user@example.com', // Placeholder
    location: '', // Optional
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsEditing(false);
    setSaveMessage('Profile updated successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  return (
    <div className="account-page">
      <div className="account-container">
        {saveMessage && (
          <div className="save-message">
            {saveMessage}
          </div>
        )}
        <div className="account-content">
          {/* Profile Section */}
          <section className="profile-section">
            <div className="profile-picture">
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="1.5"
              >
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
              {isEditing && (
                <button className="change-photo-btn" onClick={() => {}}>
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2"
                  >
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                    <circle cx="12" cy="13" r="4"/>
                  </svg>
                  Change Photo
                </button>
              )}
            </div>
            <div className="profile-info">
              <h2>{profile.name}</h2>
              <p className="profile-email">{profile.email}</p>
              <button 
                className="edit-profile-btn"
                onClick={() => setIsEditing(!isEditing)}
              >
                {isEditing ? 'Cancel Editing' : 'Edit Profile'}
              </button>
            </div>
          </section>

          {/* Personal Information Section */}
          <section className="settings-section">
            <h2>Personal Information</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  className="form-input"
                  value={profile.name}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                />
              </div>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="form-input"
                  value={profile.email}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                />
              </div>
              <div className="form-group">
                <label htmlFor="location">Location (Optional)</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  className="form-input"
                  value={profile.location}
                  onChange={handleInputChange}
                  placeholder="Enter your location for better price filtering"
                  disabled={!isEditing}
                />
              </div>
              {isEditing && (
                <button type="submit" className="save-button">
                  Save Changes
                </button>
              )}
            </form>
          </section>
        </div>
      </div>
    </div>
  );
};