    pybullet - Python bindings for Bullet Physics Robotics API (also known as Shared Memory API)

CLASSES
    builtins.Exception(builtins.BaseException)
        error

    class error(builtins.Exception)
     |  Method resolution order:
     |      error
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |
     |  Data descriptors defined here:
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.Exception:
     |
     |  __init__(self, /, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |
     |  __reduce__(...)
     |      Helper for pickle.
     |
     |  __repr__(self, /)
     |      Return repr(self).
     |
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |
     |  __setstate__(...)
     |
     |  __str__(self, /)
     |      Return str(self).
     |
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |
     |  __cause__
     |      exception cause
     |
     |  __context__
     |      exception context
     |
     |  __dict__
     |
     |  __suppress_context__
     |
     |  __traceback__
     |
     |  args

FUNCTIONS
    addUserData(...)
        addUserData(bodyUniqueId, key, value, linkIndex=-1, visualShapeIndex=-1, physicsClientId=0)
        Adds or updates a user data entry. Returns user data identifier.

    addUserDebugLine(...)
        Add a user debug draw line with lineFrom[3], lineTo[3], lineColorRGB[3], lineWidth, lifeTime. A lifeTime of 0 means permanent until removed. Returns a unique id for the user debug item.

    addUserDebugParameter(...)
        Add a user debug parameter, such as a slider, that can be controlled using a GUI.

    addUserDebugPoints(...)
        Add user debug draw points with pointPositions[3], pointColorsRGB[3], pointSize, lifeTime. A lifeTime of 0 means permanent until removed. Returns a unique id for the user debug item.

    addUserDebugText(...)
        Add a user debug draw line with text, textPosition[3], textSize and lifeTime in seconds A lifeTime of 0 means permanent until removed. Returns a unique id for the user debug item.

    applyExternalForce(...)
        for objectUniqueId, linkIndex (-1 for base/root link), apply a force [x,y,z] at the a position [x,y,z], flag to select FORCE_IN_LINK_FRAME or WORLD_FRAME coordinates

    applyExternalTorque(...)
        for objectUniqueId, linkIndex (-1 for base/root link) apply a torque [x,y,z] in Cartesian coordinates, flag to select TORQUE_IN_LINK_FRAME or WORLD_FRAME coordinates

    calculateInverseDynamics(...)
        Given an object id, joint positions, joint velocities and joint accelerations, compute the joint forces using Inverse Dynamics

    calculateInverseKinematics(...)
        Inverse Kinematics bindings: Given an object id, current joint positions and target position for the end effector,compute the inverse kinematics and return the new joint state

    calculateInverseKinematics2(...)
        Inverse Kinematics bindings: Given an object id, current joint positions and target positions for the end effectors,compute the inverse kinematics and return the new joint state

    calculateJacobian(...)
        linearJacobian, angularJacobian = calculateJacobian(bodyUniqueId, linkIndex, localPosition, objPositions, objVelocities, objAccelerations, physicsClientId=0)
        Compute the jacobian for a specified local position on a body and its kinematics.
        Args:
          bodyIndex - a scalar defining the unique object id.
          linkIndex - a scalar identifying the link containing the local point.
          localPosition - a list of [x, y, z] of the coordinates defined in the link frame.
          objPositions - a list of the joint positions.
          objVelocities - a list of the joint velocities.
          objAccelerations - a list of the joint accelerations.
        Returns:
          linearJacobian - a list of the partial linear velocities of the jacobian.
          angularJacobian - a list of the partial angular velocities of the jacobian.

    calculateMassMatrix(...)
        massMatrix = calculateMassMatrix(bodyUniqueId, objPositions, physicsClientId=0)
        Compute the mass matrix for an object and its chain of bodies.
        Args:
          bodyIndex - a scalar defining the unique object id.
          objPositions - a list of the joint positions.
        Returns:
          massMatrix - a list of lists of the mass matrix components.

    calculateVelocityQuaternion(...)
        Compute the angular velocity given start and end quaternion and delta time.

    changeConstraint(...)
        Change some parameters of an existing constraint, such as the child pivot or child frame orientation, using its unique id.

    changeDynamics(...)
        change dynamics information such as mass, lateral friction coefficient.

    changeTexture(...)
        Change a texture file.

    changeVisualShape(...)
        Change part of the visual shape information for one object.

    computeDofCount(...)
        computeDofCount returns the number of degrees of freedom, including 7 degrees of freedom for the base in case of floating base

    computeProjectionMatrix(...)
        Compute a camera projection matrix from screen left/right/bottom/top/near/far values

    computeProjectionMatrixFOV(...)
        Compute a camera projection matrix from fov, aspect ratio, near, far values

    computeViewMatrix(...)
        Compute a camera viewmatrix from camera eye,  target position and up vector

    computeViewMatrixFromYawPitchRoll(...)
        Compute a camera viewmatrix from camera eye,  target position and up vector

    configureDebugVisualizer(...)
        For the 3D OpenGL Visualizer, enable/disable GUI, shadows.

    connect(...)
        connect(method, key=SHARED_MEMORY_KEY, options='')
        connect(method, hostname='localhost', port=1234, options='')
        Connect to an existing physics server (using shared memory by default).

    createCollisionShape(...)
        Create a collision shape. Returns a non-negative (int) unique id, if successfull, negative otherwise.

    createCollisionShapeArray(...)
        Create collision shapes. Returns a non-negative (int) unique id, if successfull, negative otherwise.

    createConstraint(...)
        Create a constraint between two bodies. Returns a (int) unique id, if successfull.

    createMultiBody(...)
        Create a multi body. Returns a non-negative (int) unique id, if successfull, negative otherwise.

    createSoftBodyAnchor(...)
        Create an anchor (attachment) between a soft body and a rigid or multi body.

    createVisualShape(...)
        Create a visual shape. Returns a non-negative (int) unique id, if successfull, negative otherwise.

    createVisualShapeArray(...)
        Create visual shapes. Returns a non-negative (int) unique id, if successfull, negative otherwise.

    disconnect(...)
        disconnect(physicsClientId=0)
        Disconnect from the physics server.

    enableJointForceTorqueSensor(...)
        Enable or disable a joint force/torque sensor measuring the joint reaction forces.

    executePluginCommand(...)
        Execute a command, implemented in a plugin.

    getAABB(...)
        Get the axis aligned bound box min and max coordinates in world space.

    getAPIVersion(...)
        Get version of the API. Compatibility exists for connections using the same API version. Make sure both client and server use the same number of bits (32-bit or 64bit).

    getAxisAngleFromQuaternion(...)
        Compute the quaternion from axis and angle representation.

    getAxisDifferenceQuaternion(...)
        Compute the velocity axis difference from two quaternions.

    getBasePositionAndOrientation(...)
        Get the world position and orientation of the base of the object. (x,y,z) position vector and (x,y,z,w) quaternion orientation.

    getBaseVelocity(...)
        Get the linear and angular velocity of the base of the object  in world space coordinates. (x,y,z) linear velocity vector and (x,y,z) angular velocity vector.

    getBodyInfo(...)
        Get the body info, given a body unique id.

    getBodyUniqueId(...)
        getBodyUniqueId is used after connecting to server with existing bodies.Get the unique id of the body, given a integer range [0.. number of bodies).

    getCameraImage(...)
        Render an image (given the pixel resolution width, height, camera viewMatrix , projectionMatrix, lightDirection, lightColor, lightDistance, shadow, lightAmbientCoeff, lightDiffuseCoeff, lightSpecularCoeff, and renderer), and return the 8-8-8bit RGB pixel data and floating point depth values as NumPy arrays

    getClosestPoints(...)
        Compute the closest points between two objects, if the distance is below a given threshold.Input is two objects unique ids and distance threshold.

    getCollisionShapeData(...)
        Return the collision shape information for one object.

    getConnectionInfo(...)
        getConnectionInfo(physicsClientId=0)
        Return if a given client id is connected, and using what method.

    getConstraintInfo(...)
        Get the user-created constraint info, given a constraint unique id.

    getConstraintState(...)
        Get the user-created constraint state (applied forces), given a constraint unique id.

    getConstraintUniqueId(...)
        Get the unique id of the constraint, given a integer index in range [0.. number of constraints).

    getContactPoints(...)
        Return existing contact points after the stepSimulation command. Optional arguments one or two object unique ids, that need to be involved in the contact.

    getDebugVisualizerCamera(...)
        Get information about the 3D visualizer camera, such as width, height, view matrix, projection matrix etc.

    getDifferenceQuaternion(...)
        Compute the quaternion difference from two quaternions.

    getDynamicsInfo(...)
        Get dynamics information such as mass, lateral friction coefficient.

    getEulerFromQuaternion(...)
        Convert quaternion [x,y,z,w] to Euler [roll, pitch, yaw] as in URDF/SDF convention

    getJointInfo(...)
        Get the name and type info for a joint on a body.

    getJointState(...)
        Get the state (position, velocity etc) for a joint on a body.

    getJointStateMultiDof(...)
        Get the state (position, velocity etc) for a joint on a body. (supports planar and spherical joints)

    getJointStates(...)
        Get the state (position, velocity etc) for multiple joints on a body.

    getJointStatesMultiDof(...)
        Get the states (position, velocity etc) for multiple joint on a body. (supports planar and spherical joints)

    getKeyboardEvents(...)
        Get keyboard events, keycode and state (KEY_IS_DOWN, KEY_WAS_TRIGGERED, KEY_WAS_RELEASED)

    getLinkState(...)
        position_linkcom_world, world_rotation_linkcom,
        position_linkcom_frame, frame_rotation_linkcom,
        position_frame_world, world_rotation_frame,
        linearVelocity_linkcom_world, angularVelocity_linkcom_world
          = getLinkState(objectUniqueId, linkIndex, computeLinkVelocity=0,
                         computeForwardKinematics=0, physicsClientId=0)
        Provides extra information such as the Cartesian world coordinates center of mass (COM) of the link, relative to the world reference frame.

    getLinkStates(...)
        same as getLinkState except it takes a list of linkIndices

    getMatrixFromQuaternion(...)
        Compute the 3x3 matrix from a quaternion, as a list of 9 values (row-major)

    getMeshData(...)
        Get mesh data. Returns vertices etc from the mesh.

    getMouseEvents(...)
        Get mouse events, event type and button state (KEY_IS_DOWN, KEY_WAS_TRIGGERED, KEY_WAS_RELEASED)

    getNumBodies(...)
        Get the number of bodies in the simulation.

    getNumConstraints(...)
        Get the number of user-created constraints in the simulation.

    getNumJoints(...)
        Get the number of joints for an object.

    getNumUserData(...)
        getNumUserData(bodyUniqueId physicsClientId=0)
        Retrieves the number of user data entries in a body.

    getOverlappingObjects(...)
        Return all the objects that have overlap with a given axis-aligned bounding box volume (AABB).Input are two vectors defining the AABB in world space [min_x,min_y,min_z],[max_x,max_y,max_z].

    getPhysicsEngineParameters(...)
        Get the current values of internal physics engine parameters

    getQuaternionFromAxisAngle(...)
        Compute the quaternion from axis and angle representation.

    getQuaternionFromEuler(...)
        Convert Euler [roll, pitch, yaw] as in URDF/SDF convention, to quaternion [x,y,z,w]

    getQuaternionSlerp(...)
        Compute the spherical interpolation given a start and end quaternion and an interpolation value in range [0..1]

    getTetraMeshData(...)
        Get mesh data. Returns tetra from the mesh.

    getUserData(...)
        getUserData(userDataId, physicsClientId=0)
        Returns the user data value.

    getUserDataId(...)
        getUserDataId(bodyUniqueId, key, linkIndex=-1, visualShapeIndex=-1, physicsClientId=0)
        Retrieves the userDataId given the key and optionally link and visual shape index.

    getUserDataInfo(...)
        getUserDataInfo(bodyUniqueId, userDataIndex, physicsClientId=0)
        Retrieves the key and the identifier of a user data as (userDataId, key, bodyUniqueId, linkIndex, visualShapeIndex).

    getVREvents(...)
        Get Virtual Reality events, for example to track VR controllers position/buttons

    getVisualShapeData(...)
        Return the visual shape information for one object.

    invertTransform(...)
        Invert a transform, provided as [position], [quaternion].

    isConnected(...)
        isConnected(physicsClientId=0)
        Return if a given client id is connected.

    isNumpyEnabled(...)
        return True if PyBullet was compiled with NUMPY support. This makes the getCameraImage API faster

    loadBullet(...)
        Load a world from a .bullet file.

    loadMJCF(...)
        Load multibodies from an MJCF file.

    loadPlugin(...)
        Load a plugin, could implement custom commands etc.

    loadSDF(...)
        Load multibodies from an SDF file.

    loadSoftBody(...)
        Load a softbody from an obj file.

    loadTexture(...)
        Load texture file.

    loadURDF(...)
        bodyUniqueId = loadURDF(fileName, basePosition=[0.,0.,0.], baseOrientation=[0.,0.,0.,1.], useMaximalCoordinates=0, useFixedBase=0, flags=0, globalScaling=1.0, physicsClientId=0)
        Create a multibody by loading a URDF file.

    multiplyTransforms(...)
        Multiply two transform, provided as [position], [quaternion].

    performCollisionDetection(...)
        performCollisionDetection(physicsClientId=0)
        Update AABBs, compute overlapping pairs and contact points. stepSimulation also includes this already.

    rayTest(...)
        Cast a ray and return the first object hit, if any. Takes two arguments (from_position [x,y,z] and to_position [x,y,z] in Cartesian world coordinates

    rayTestBatch(...)
        Cast a batch of rays and return the result for each of the rays (first object hit, if any. or -1) Takes two required arguments (list of from_positions [x,y,z] and a list of to_positions [x,y,z] in Cartesian world coordinates) and one optional argument numThreads to specify the number of threads to use to compute the ray intersections for the batch. Specify 0 to let Bullet decide, 1 (default) for single core execution, 2 or more to select the number of threads to use.

    readUserDebugParameter(...)
        Read the current value of a user debug parameter, given the user debug item unique id.

    removeAllUserDebugItems(...)
        remove all user debug draw items

    removeAllUserParameters(...)
        remove all user debug parameters (sliders, buttons)

    removeBody(...)
        Remove a body by its body unique id.

    removeCollisionShape(...)
        Remove a collision shape. Only useful when the collision shape is not used in a body (to perform a getClosestPoint query).

    removeConstraint(...)
        Remove a constraint using its unique id.

    removeState(...)
        Remove a state created using saveState by its state unique id.

    removeUserData(...)
        removeUserData(userDataId, physicsClientId=0)
        Removes a user data entry.

    removeUserDebugItem(...)
        remove a user debug draw item, giving its unique id

    renderImage(...)
        obsolete, please use getCameraImage and getViewProjectionMatrices instead

    resetBasePositionAndOrientation(...)
        Reset the world position and orientation of the base of the object instantaneously, not through physics simulation. (x,y,z) position vector and (x,y,z,w) quaternion orientation.

    resetBaseVelocity(...)
        Reset the linear and/or angular velocity of the base of the object  in world space coordinates. linearVelocity (x,y,z) and angularVelocity (x,y,z).

    resetDebugVisualizerCamera(...)
        For the 3D OpenGL Visualizer, set the camera distance, yaw, pitch and target position.

    resetJointState(...)
        resetJointState(objectUniqueId, jointIndex, targetValue, targetVelocity=0, physicsClientId=0)
        Reset the state (position, velocity etc) for a joint on a body instantaneously, not through physics simulation.

    resetJointStateMultiDof(...)
        resetJointStateMultiDof(objectUniqueId, jointIndex, targetValue, targetVelocity=0, physicsClientId=0)
        Reset the state (position, velocity etc) for a joint on a body instantaneously, not through physics simulation.

    resetJointStatesMultiDof(...)
        resetJointStatesMultiDof(objectUniqueId, jointIndices, targetValues, targetVelocities=0, physicsClientId=0)
        Reset the states (position, velocity etc) for multiple joints on a body instantaneously, not through physics simulation.

    resetMeshData(...)
        Reset mesh data. Only implemented for deformable bodies.

    resetSimulation(...)
        resetSimulation(physicsClientId=0)
        Reset the simulation: remove all objects and start from an empty world.

    resetVisualShapeData(...)
        Obsolete method, kept for backward compatibility, use changeVisualShapeData instead.

    restoreState(...)
        Restore the full state of an existing world.

    rotateVector(...)
        Rotate a vector using a quaternion.

    saveBullet(...)
        Save the full state of the world to a .bullet file.

    saveState(...)
        Save the full state of the world to memory.

    saveWorld(...)
        Save a approximate Python file to reproduce the current state of the world: saveWorld(filename). (very preliminary and approximately)

    setAdditionalSearchPath(...)
        Set an additional search path, used to load URDF/SDF files.

    setCollisionFilterGroupMask(...)
        Set the collision filter group and the mask for a body.

    setCollisionFilterPair(...)
        Enable or disable collision detection between two object links.Input are two object unique ids and two link indices and an enumto enable or disable collisions.

    setDebugObjectColor(...)
        Override the wireframe debug drawing color for a particular object unique id / link index.If you ommit the color, the custom color will be removed.

    setDefaultContactERP(...)
        setDefaultContactERP(defaultContactERP, physicsClientId=0)
        Set the amount of contact penetration Error Recovery Paramater (ERP) in each time step.                 This is an tuning parameter to control resting contact stability. This value depends on the time step.

    setGravity(...)
        setGravity(gravX, gravY, gravZ, physicsClientId=0)
        Set the gravity acceleration (x,y,z).

    setInternalSimFlags(...)
        This is for experimental purposes, use at own risk, magic may or not happen

    setJointMotorControl(...)
        This (obsolete) method cannot select non-zero physicsClientId, use setJointMotorControl2 instead.Set a single joint motor control mode and desired target value. There is no immediate state change, stepSimulation will process the motors.

    setJointMotorControl2(...)
        Set a single joint motor control mode and desired target value. There is no immediate state change, stepSimulation will process the motors.

    setJointMotorControlArray(...)
        Set an array of motors control mode and desired target value. There is no immediate state change, stepSimulation will process the motors.This is similar to setJointMotorControl2, with jointIndices as a list, and optional targetPositions, targetVelocities, forces, kds and kps as listsUsing setJointMotorControlArray has the benefit of lower calling overhead.

    setJointMotorControlMultiDof(...)
        Set a single joint motor control mode and desired target value. There is no immediate state change, stepSimulation will process the motors.This method sets multi-degree-of-freedom motor such as the spherical joint motor.

    setJointMotorControlMultiDofArray(...)
        Set control mode and desired target values for multiple motors. There is no immediate state change, stepSimulation will process the motors.This method sets multi-degree-of-freedom motor such as the spherical joint motor.

    setPhysicsEngineParameter(...)
        Set some internal physics engine parameter, such as cfm or erp etc.

    setRealTimeSimulation(...)
        setRealTimeSimulation(enableRealTimeSimulation, physicsClientId=0)
        Enable or disable real time simulation (using the real time clock, RTC) in the physics server. Expects one integer argument, 0 or 1

    setTimeOut(...)
        Set the timeOut in seconds, used for most of the API calls.

    setTimeStep(...)
        setTimeStep(timestep, physicsClientId=0)
        Set the amount of time to proceed at each call to stepSimulation. (unit is seconds, typically range is 0.01 or 0.001)

    setVRCameraState(...)
        Set properties of the VR Camera such as its root transform for teleporting or to track objects (camera inside a vehicle for example).

    startStateLogging(...)
        Start logging of state, such as robot base position, orientation, joint positions etc. Specify loggingType (STATE_LOGGING_MINITAUR, STATE_LOGGING_GENERIC_ROBOT, STATE_LOGGING_VR_CONTROLLERS, STATE_LOGGING_CONTACT_POINTS, etc), fileName, optional objectUniqueId, maxLogDof, bodyUniqueIdA, bodyUniqueIdB, linkIndexA, linkIndexB. Function returns int loggingUniqueId

    stepSimulation(...)
        stepSimulation(physicsClientId=0)
        Step the simulation using forward dynamics.

    stopStateLogging(...)
        Stop logging of robot state, given a loggingUniqueId.

    submitProfileTiming(...)
        Add a custom profile timing that will be visible in performance profile recordings on the physics server.On the physics server (in GUI and VR mode) you can press 'p' to start and/or stop profile recordings

    syncBodyInfo(...)
        syncBodyInfo(physicsClientId=0)
        Update body and constraint/joint information, in case other clients made changes.

    syncUserData(...)
        syncUserData(bodyUniqueIds=[], physicsClientId=0)
        Update user data, in case other clients made changes.

    unloadPlugin(...)
        Unload a plugin, given the pluginUniqueId.

    unsupportedChangeScaling(...)
        Change the scaling of the base of an object.Warning: unsupported rudimentary feature that has many limitations.

    vhacd(...)
        Compute volume hierarchical convex decomposition of an OBJ file.

DATA
    ACTIVATION_STATE_DISABLE_SLEEPING = 2
    ACTIVATION_STATE_DISABLE_WAKEUP = 32
    ACTIVATION_STATE_ENABLE_SLEEPING = 1
    ACTIVATION_STATE_ENABLE_WAKEUP = 16
    ACTIVATION_STATE_SLEEP = 8
    ACTIVATION_STATE_WAKE_UP = 4
    AddFileIOAction = 1024
    B3G_ALT = 65308
    B3G_BACKSPACE = 65305
    B3G_CONTROL = 65307
    B3G_DELETE = 65304
    B3G_DOWN_ARROW = 65298
    B3G_END = 65301
    B3G_F1 = 65280
    B3G_F10 = 65289
    B3G_F11 = 65290
    B3G_F12 = 65291
    B3G_F13 = 65292
    B3G_F14 = 65293
    B3G_F15 = 65294
    B3G_F2 = 65281
    B3G_F3 = 65282
    B3G_F4 = 65283
    B3G_F5 = 65284
    B3G_F6 = 65285
    B3G_F7 = 65286
    B3G_F8 = 65287
    B3G_F9 = 65288
    B3G_HOME = 65302
    B3G_INSERT = 65303
    B3G_LEFT_ARROW = 65295
    B3G_PAGE_DOWN = 65300
    B3G_PAGE_UP = 65299
    B3G_RETURN = 65309
    B3G_RIGHT_ARROW = 65296
    B3G_SHIFT = 65306
    B3G_SPACE = 32
    B3G_UP_ARROW = 65297
    CNSFileIO = 3
    CONSTRAINT_SOLVER_LCP_DANTZIG = 3
    CONSTRAINT_SOLVER_LCP_PGS = 2
    CONSTRAINT_SOLVER_LCP_SI = 1
    CONTACT_RECOMPUTE_CLOSEST = 1
    CONTACT_REPORT_EXISTING = 0
    COV_ENABLE_DEPTH_BUFFER_PREVIEW = 14
    COV_ENABLE_GUI = 1
    COV_ENABLE_KEYBOARD_SHORTCUTS = 9
    COV_ENABLE_MOUSE_PICKING = 10
    COV_ENABLE_PLANAR_REFLECTION = 16
    COV_ENABLE_RENDERING = 7
    COV_ENABLE_RGB_BUFFER_PREVIEW = 13
    COV_ENABLE_SEGMENTATION_MARK_PREVIEW = 15
    COV_ENABLE_SHADOWS = 2
    COV_ENABLE_SINGLE_STEP_RENDERING = 17
    COV_ENABLE_TINY_RENDERER = 12
    COV_ENABLE_VR_PICKING = 5
    COV_ENABLE_VR_RENDER_CONTROLLERS = 6
    COV_ENABLE_VR_TELEPORTING = 4
    COV_ENABLE_WIREFRAME = 3
    COV_ENABLE_Y_AXIS_UP = 11
    DIRECT = 2
    ER_BULLET_HARDWARE_OPENGL = 131072
    ER_NO_SEGMENTATION_MASK = 4
    ER_SEGMENTATION_MASK_OBJECT_AND_LINKINDEX = 1
    ER_TINY_RENDERER = 65536
    ER_USE_PROJECTIVE_TEXTURE = 2
    GEOM_BOX = 3
    GEOM_CAPSULE = 7
    GEOM_CONCAVE_INTERNAL_EDGE = 2
    GEOM_CYLINDER = 4
    GEOM_FORCE_CONCAVE_TRIMESH = 1
    GEOM_HEIGHTFIELD = 9
    GEOM_MESH = 5
    GEOM_PLANE = 6
    GEOM_SPHERE = 2
    GRAPHICS_CLIENT = 14
    GRAPHICS_SERVER = 15
    GRAPHICS_SERVER_MAIN_THREAD = 17
    GRAPHICS_SERVER_TCP = 16
    GUI = 1
    GUI_MAIN_THREAD = 8
    GUI_SERVER = 7
    IK_DLS = 0
    IK_HAS_JOINT_DAMPING = 128
    IK_HAS_NULL_SPACE_VELOCITY = 64
    IK_HAS_TARGET_ORIENTATION = 32
    IK_HAS_TARGET_POSITION = 16
    IK_SDLS = 1
    JOINT_FEEDBACK_IN_JOINT_FRAME = 2
    JOINT_FEEDBACK_IN_WORLD_SPACE = 1
    JOINT_FIXED = 4
    JOINT_GEAR = 6
    JOINT_PLANAR = 3
    JOINT_POINT2POINT = 5
    JOINT_PRISMATIC = 1
    JOINT_REVOLUTE = 0
    JOINT_SPHERICAL = 2
    KEY_IS_DOWN = 1
    KEY_WAS_RELEASED = 4
    KEY_WAS_TRIGGERED = 2
    LINK_FRAME = 1
    MAX_RAY_INTERSECTION_BATCH_SIZE = 16384
    MESH_DATA_SIMULATION_MESH = 1
    MJCF_COLORS_FROM_FILE = 512
    PD_CONTROL = 3
    POSITION_CONTROL = 2
    PosixFileIO = 1
    RESET_USE_DEFORMABLE_WORLD = 1
    RESET_USE_DISCRETE_DYNAMICS_WORLD = 2
    RESET_USE_REDUCED_DEFORMABLE_WORLD = 8
    RESET_USE_SIMPLE_BROADPHASE = 4
    RemoveFileIOAction = 1025
    SENSOR_FORCE_TORQUE = 1
    SHARED_MEMORY = 3
    SHARED_MEMORY_GUI = 14
    SHARED_MEMORY_KEY = 12347
    SHARED_MEMORY_KEY2 = 12348
    SHARED_MEMORY_SERVER = 9
    STABLE_PD_CONTROL = 4
    STATE_LOGGING_ALL_COMMANDS = 7
    STATE_LOGGING_CONTACT_POINTS = 5
    STATE_LOGGING_CUSTOM_TIMER = 9
    STATE_LOGGING_GENERIC_ROBOT = 1
    STATE_LOGGING_MINITAUR = 0
    STATE_LOGGING_PROFILE_TIMINGS = 6
    STATE_LOGGING_VIDEO_MP4 = 3
    STATE_LOGGING_VR_CONTROLLERS = 2
    STATE_LOG_JOINT_MOTOR_TORQUES = 1
    STATE_LOG_JOINT_TORQUES = 3
    STATE_LOG_JOINT_USER_TORQUES = 2
    STATE_REPLAY_ALL_COMMANDS = 8
    TCP = 5
    TORQUE_CONTROL = 1
    UDP = 4
    URDF_ENABLE_CACHED_GRAPHICS_SHAPES = 1024
    URDF_ENABLE_SLEEPING = 2048
    URDF_ENABLE_WAKEUP = 262144
    URDF_GLOBAL_VELOCITIES_MB = 256
    URDF_GOOGLEY_UNDEFINED_COLORS = 8388608
    URDF_IGNORE_COLLISION_SHAPES = 2097152
    URDF_IGNORE_VISUAL_SHAPES = 1048576
    URDF_INITIALIZE_SAT_FEATURES = 4096
    URDF_MAINTAIN_LINK_ORDER = 131072
    URDF_MERGE_FIXED_LINKS = 524288
    URDF_PRINT_URDF_INFO = 4194304
    URDF_USE_IMPLICIT_CYLINDER = 128
    URDF_USE_INERTIA_FROM_FILE = 2
    URDF_USE_MATERIAL_COLORS_FROM_MTL = 32768
    URDF_USE_MATERIAL_TRANSPARANCY_FROM_MTL = 65536
    URDF_USE_SELF_COLLISION = 8
    URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS = 32
    URDF_USE_SELF_COLLISION_EXCLUDE_PARENT = 16
    URDF_USE_SELF_COLLISION_INCLUDE_PARENT = 8192
    VELOCITY_CONTROL = 0
    VISUAL_SHAPE_DATA_TEXTURE_UNIQUE_IDS = 1
    VISUAL_SHAPE_DOUBLE_SIDED = 4
    VR_BUTTON_IS_DOWN = 1
    VR_BUTTON_WAS_RELEASED = 4
    VR_BUTTON_WAS_TRIGGERED = 2
    VR_CAMERA_TRACK_OBJECT_ORIENTATION = 1
    VR_DEVICE_CONTROLLER = 1
    VR_DEVICE_GENERIC_TRACKER = 4
    VR_DEVICE_HMD = 2
    VR_MAX_BUTTONS = 64
    VR_MAX_CONTROLLERS = 8
    WORLD_FRAME = 2
    ZipFileIO = 2