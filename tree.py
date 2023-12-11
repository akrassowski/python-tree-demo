#!/usr/bin/env python
"""Publish shapes to form a Christmas Tree"""
import argparse
import signal, sys
import time
import rti.connextdds as dds

SHAPE_TYPE = dds.QosProvider("tree.xml").type("tree_lib", "ShapeType")
HANDLE = dds.InstanceHandle.nil()

def update_and_write(instance, writer, x, y):
    """Helper to update and write a sample"""
    instance.set_int("x", x)
    instance.set_int("y", y)
    writer.write(instance, HANDLE)

def draw_tree(writer):
    """Draw the large triangle and some detail branches"""
    instance = dds.DynamicData(SHAPE_TYPE)
    instance.set_string("color", "GREEN")
    instance.set_int("shapesize", 200)
    update_and_write(instance, writer, 128, 120)
    loc = [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    size = 20
    instance.set_string("color", "GREEN")
    instance.set_int("shapesize", size)
    delta_x, delta_y = (size * 0.50), size
    start_x, y = 122-((delta_x * 0.5 * len(loc[0]))), 38
    for row in loc:
        x = start_x
        for item in row:
            x += delta_x
            if item:
                update_and_write(instance, writer, int(x), int(y))
        y += delta_y


def draw_trunk(writer):
    """Draw the trunk as a Square."""
    instance = dds.DynamicData(SHAPE_TYPE)
    instance.set_string("color", "BROWN")
    size = 40
    x, y = 128, 235

    instance.set_int("shapesize", size)
    update_and_write(instance, writer, x, y)

def draw_balls(writer):
    """Draw some balls in red."""
    instance = dds.DynamicData(SHAPE_TYPE)
    size = 10
    start_x1 = 105
    start_x2 = start_x1 - (size * 4)
    start_x3 = start_x2 - (size * 3)
    pos = [
        [start_x1, 83],
        [size * 1.5 + start_x1, 83 + size],
        [size * 3.0 + start_x1, 83],
        [size * 4.5 + start_x1, 83 + size],

        [size * 1.5 + start_x2, 123 + size],
        [size * 3.0 + start_x2, 123],
        [size * 4.5 + start_x2, 123 + size],
        [size * 6.0 + start_x2, 123],
        [size * 7.5 + start_x2, 123 + size],
        [size * 9.0 + start_x2, 123],
        [size * 10.5 + start_x2, 123 + size],

        [size * 1.5 + start_x3, 173 + size],
        [size * 3.0 + start_x3, 173],
        [size * 4.5 + start_x3, 173 + size],
        [size * 6.0 + start_x3, 173],
        [size * 7.5 + start_x3, 173 + size],
        [size * 9.0 + start_x3, 173],
        [size * 10.5 + start_x3, 173 + size],
        [size * 12.0 + start_x3, 173],
        [size * 13.5 + start_x3, 173 + size],
        [size * 15.0 + start_x3, 173],
        [size * 16.5 + start_x3, 173 + size],
    ]
    instance.set_int("shapesize", size)
    instance.set_string("color", "RED")
    for x, y in pos:
        update_and_write(instance, writer, int(x), int(y))
        # time.sleep(0.5)

def draw_topper(writer):
    """Draw the tree topper"""
    instance = dds.DynamicData(SHAPE_TYPE)
    instance.set_string("color", "YELLOW")
    size, x, y = 30, 128, 15
    instance.set_int("shapesize", size)
    update_and_write(instance, writer, x, y)

def publisher_main(domain_id):
    participant = dds.DomainParticipant(domain_id)
    writer_qos = dds.QosProvider.default.datawriter_qos
    tree_topic = dds.DynamicData.Topic(participant, "Triangle", SHAPE_TYPE)
    tree_writer = dds.DynamicData.DataWriter(dds.Publisher(participant), tree_topic, writer_qos)

    trunk_topic = dds.DynamicData.Topic(participant, "Square", SHAPE_TYPE)
    trunk_writer = dds.DynamicData.DataWriter(dds.Publisher(participant), trunk_topic, writer_qos)

    ball_topic = dds.DynamicData.Topic(participant, "Circle", SHAPE_TYPE)
    ball_writer = dds.DynamicData.DataWriter(dds.Publisher(participant), ball_topic, writer_qos)

    while 1:
        draw_trunk(trunk_writer)
        draw_tree(tree_writer)
        #draw_balls(ball_writer)
        draw_balls(ball_writer)
        for n in range(5):
            draw_balls(ball_writer)
            draw_topper(ball_writer)
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="RTI Connext DDS Publish Tree"
    )
    parser.add_argument("-d", "--domain", type=int, default=0, help="DDS Domain ID")

    args = parser.parse_args()
    assert 0 <= args.domain < 233

    print("""
    This Python program will publish multiple colored shapes.
    Run the Shapes Demo and subscribe to Square.
    Also subscribe to Triangle and Circle with a depth of 200.
    When that's running, hit the Enter key to continue.""", flush=True)
    input()
    print("""Use Control-C to terminate.""", flush=True)
    try:
        publisher_main(args.domain)
    except KeyboardInterrupt as e:
        pass
    print("...exiting...")
    sys.exit(0)

