import tensorflow as tf
import numpy as np

states = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
NUM_STATES = len(states)
NUM_ACTIONS = 2
DISCOUNT_FACTOR = 0.5


def hot_one_state(index):
    array = np.zeros(NUM_STATES)
    array[index] = 1.
    return array


session = tf.Session()
state = tf.placeholder("float", [None, NUM_STATES])
targets = tf.placeholder("float", [None, NUM_ACTIONS])

weights = tf.Variable(tf.constant(0., shape=[NUM_STATES, NUM_ACTIONS]))

output = tf.matmul(state, weights)

loss = tf.reduce_mean(tf.square(output - targets))
train_operation = tf.train.GradientDescentOptimizer(1.).minimize(loss)

session.run(tf.initialize_all_variables())

for _ in range(50):
    state_batch = []
    rewards_batch = []

    for state_index in range(NUM_STATES):
        state_batch.append(hot_one_state(state_index))

        minus_action_index = (state_index - 1) % NUM_STATES
        plus_action_index = (state_index + 1) % NUM_STATES

        minus_action_state_reward = session.run(output, feed_dict={state: [hot_one_state(minus_action_index)]})
        plus_action_state_reward = session.run(output, feed_dict={state: [hot_one_state(plus_action_index)]})

        minus_action_q_value = DISCOUNT_FACTOR * (states[minus_action_index] + np.max(minus_action_state_reward))
        plus_action_q_value = DISCOUNT_FACTOR * (states[plus_action_index] + np.max(plus_action_state_reward))

        action_rewards = [minus_action_q_value, plus_action_q_value]
        rewards_batch.append(action_rewards)

    session.run(train_operation, feed_dict={
        state: state_batch,
        targets: rewards_batch})

    print([states[x] + np.max(session.run(output, feed_dict={state: [hot_one_state(x)]}))
           for x in range(NUM_STATES)])
