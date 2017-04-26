Glossary
========

.. glossary::
    acoustic scene
        Descriptor for surrounding audio environment, for example "outdoor market", "busy street", "office".

    event label
        Textual description of sound event, usually one or two words.

    event offset
        End of the event instance as a time-stamp (in seconds).

    event onset
        Start of the event instance as a time-stamp (in seconds).

    macro-average
        Intermediate statistics are aggregated class-wise, class-based metrics are calculated,
        then average of class based metrics; each class has equal influence on the final metric value. (see :ref:`averaging`)

    micro-average
        Intermediate statistics are aggregated over all test data, then metrics are calculated;
        each instance has equal influence on the final metric value. (see :ref:`averaging`)

    scene label
        Textual label used to identify acoustic scene.

    sound event
        Audio segment that is attributed to a specific sound source and is perceived as an entity.
        Marked as having onset and offset and labeled with textual descriptors related to the sound source,
        for example "dog barking", "car passing by".

