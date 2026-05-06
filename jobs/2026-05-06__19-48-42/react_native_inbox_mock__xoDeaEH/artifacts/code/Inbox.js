import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, FlatList, TouchableOpacity, ActivityIndicator } from 'react-native';

// Use placeholders for MagicBell API Key and User Email as they were not explicitly provided in the environment.
const MAGICBELL_API_KEY = 'YOUR_MAGICBELL_API_KEY';
const MAGICBELL_USER_EMAIL = 'YOUR_MAGICBELL_USER_EMAIL';

const Inbox = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchNotifications = async () => {
    try {
      const response = await fetch('https://api.magicbell.com/notifications', {
        headers: {
          'X-MAGICBELL-API-KEY': MAGICBELL_API_KEY,
          'X-MAGICBELL-USER-EMAIL': MAGICBELL_USER_EMAIL,
          'Accept': 'application/json',
        },
      });
      const data = await response.json();
      setNotifications(data.notifications || []);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const markAllAsRead = async () => {
    try {
      await fetch('https://api.magicbell.com/notifications/read', {
        method: 'POST',
        headers: {
          'X-MAGICBELL-API-KEY': MAGICBELL_API_KEY,
          'X-MAGICBELL-USER-EMAIL': MAGICBELL_USER_EMAIL,
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      });
      // Refresh notifications after marking all as read
      fetchNotifications();
    } catch (error) {
      console.error('Error marking all as read:', error);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.notificationItem}>
      <Text style={styles.notificationTitle}>{item.title}</Text>
      <Text style={styles.notificationContent}>{item.content}</Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.button} onPress={markAllAsRead}>
        <Text style={styles.buttonText}>Mark all as read</Text>
      </TouchableOpacity>
      <FlatList
        data={notifications}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        onRefresh={() => {
          setRefreshing(true);
          fetchNotifications();
        }}
        refreshing={refreshing}
        ListEmptyComponent={<Text style={styles.emptyText}>No notifications</Text>}
        contentContainerStyle={notifications.length === 0 ? { flex: 1 } : null}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: '100%',
    backgroundColor: '#f5f5f5',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notificationItem: {
    backgroundColor: '#fff',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  notificationTitle: {
    fontWeight: 'bold',
    fontSize: 16,
    color: '#333',
  },
  notificationContent: {
    marginTop: 5,
    fontSize: 14,
    color: '#666',
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 15,
    margin: 15,
    borderRadius: 8,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  emptyText: {
    textAlign: 'center',
    marginTop: 50,
    color: '#999',
    fontSize: 16,
  },
});

export default Inbox;
